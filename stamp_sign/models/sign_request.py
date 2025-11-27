import base64
import io
import time

from PIL import UnidentifiedImageError
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from odoo import _, models, Command
from odoo.tools import format_date
from odoo.exceptions import UserError, ValidationError
from odoo.tools.pdf import PdfFileReader, PdfFileWriter

try:
    from PyPDF2.errors import PdfReadError
except ImportError:
    from PyPDF2.utils import PdfReadError


def _fix_image_transparency(image):
    pixels = image.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            if pixels[x, y] == (0, 0, 0, 0):
                pixels[x, y] = (255, 255, 255, 0)


class SignRequest(models.Model):
    _inherit = "sign.request"

    def _generate_completed_document(self, password=""):
        self.ensure_one()
        self._validate_document_state()

        if not self.template_id.sign_item_ids:
            self._copy_template_to_completed_document()
        else:
            old_pdf = self._load_template_pdf(password)
            new_pdf_data = self._create_signed_overlay(old_pdf)
            self._merge_pdfs_and_store(old_pdf, new_pdf_data, password)

        attachment = self._create_attachment_from_completed_doc()
        log_attachment = self._create_completion_certificate()
        self._attach_completed_documents(attachment, log_attachment)

    def _validate_document_state(self):
        if self.state != "signed":
            raise UserError(
                _(
                    "The completed document cannot be created because the sign request is not fully signed"
                )
            )

    def _copy_template_to_completed_document(self):
        self.completed_document = self.template_id.attachment_id.datas

    def _load_template_pdf(self, password):
        try:
            pdf_reader = PdfFileReader(
                io.BytesIO(base64.b64decode(self.template_id.attachment_id.datas)),
                strict=False,
                overwriteWarnings=False,
            )
            pdf_reader.getNumPages()
        except PdfReadError:
            raise ValidationError(_("ERROR: Invalid PDF file!"))

        if pdf_reader.isEncrypted and not pdf_reader.decrypt(password):
            return  # Password invalid

        return pdf_reader

    def _create_signed_overlay(self, old_pdf):
        font = self._get_font()
        normalFontSize = self._get_normal_font_size()
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=self.get_page_size(old_pdf))
        items_by_page, values = self._collect_items_and_values()

        for p in range(0, old_pdf.getNumPages()):
            page = old_pdf.getPage(p)
            width, height = self._get_page_dimensions(page)
            self._apply_page_rotation(can, page, width, height)

            for item in items_by_page.get(p + 1, []):
                self._draw_item(
                    can, item, values.get(item.id), width, height, font, normalFontSize
                )
            can.showPage()

        can.save()
        return PdfFileReader(packet, overwriteWarnings=False)

    def _collect_items_and_values(self):
        items_by_page = self.template_id._get_sign_items_by_page()
        item_ids = [id for items in items_by_page.values() for id in items.ids]
        values_dict = self.env["sign.request.item.value"]._read_group(
            [("sign_item_id", "in", item_ids), ("sign_request_id", "=", self.id)],
            groupby=["sign_item_id"],
            aggregates=[
                "value:array_agg",
                "frame_value:array_agg",
                "frame_has_hash:array_agg",
            ],
        )
        values = {
            item: {"value": vals[0], "frame": frames[0], "frame_has_hash": hashes[0]}
            for item, vals, frames, hashes in values_dict
        }
        return items_by_page, values

    def _get_page_dimensions(self, page):
        width = float(abs(page.mediaBox.getWidth()))
        height = float(abs(page.mediaBox.getHeight()))
        return width, height

    def _apply_page_rotation(self, can, page, width, height):
        rotation = page.get("/Rotate", 0)
        if isinstance(rotation, int):
            can.rotate(rotation)
            if rotation == 90:
                width, height = height, width
                can.translate(0, -height)
            elif rotation == 180:
                can.translate(-width, -height)
            elif rotation == 270:
                width, height = height, width
                can.translate(-width, 0)

    def _draw_item(self, can, item, value_dict, width, height, font, normalFontSize):
        if not value_dict:
            return

        value, frame = value_dict["value"], value_dict["frame"]
        if frame:
            self._draw_image(can, frame, item, width, height)

        draw_method = getattr(self, f"_draw_{item.type_id.item_type}", None)
        if draw_method:
            draw_method(can, item, value, width, height, font, normalFontSize)

    def _draw_image(self, can, frame_data, item, width, height):
        try:
            image_reader = ImageReader(
                io.BytesIO(base64.b64decode(frame_data.split(",")[1]))
            )
        except UnidentifiedImageError:
            raise ValidationError(
                _(
                    "There was an issue downloading your document. Please contact an administrator."
                )
            )

        _fix_image_transparency(image_reader._image)
        can.drawImage(
            image_reader,
            width * item.posX,
            height * (1 - item.posY - item.height),
            width * item.width,
            height * item.height,
            "auto",
            True,
        )

    def _draw_signature(self, can, item, value, width, height, *_):
        self._draw_image(can, value, item, width, height)

    _draw_initial = _draw_signature
    _draw_stamp = _draw_signature

    def _merge_pdfs_and_store(self, old_pdf, overlay_pdf, password):
        new_pdf = PdfFileWriter()
        for i in range(old_pdf.getNumPages()):
            page = old_pdf.getPage(i)
            page.mergePage(overlay_pdf.getPage(i))
            new_pdf.addPage(page)
        if old_pdf.isEncrypted:
            new_pdf.encrypt(password)

        output = io.BytesIO()
        try:
            new_pdf.write(output)
        except PdfReadError:
            raise ValidationError(
                _(
                    "There was an issue downloading your document. Please contact an administrator."
                )
            )
        self.completed_document = base64.b64encode(output.getvalue())
        output.close()

    def _create_attachment_from_completed_doc(self):
        filename = (
            self.reference
            if self.reference.endswith(".pdf")
            else f"{self.reference}.pdf"
        )
        return self.env["ir.attachment"].create(
            {
                "name": filename,
                "datas": self.completed_document,
                "type": "binary",
                "res_model": self._name,
                "res_id": self.id,
            }
        )

    def _create_completion_certificate(self):
        public_user = (
            self.env.ref("base.public_user", raise_if_not_found=False) or self.env.user
        )
        pdf_content, _ = (
            self.env["ir.actions.report"]
            .with_user(public_user)
            .sudo()
            ._render_qweb_pdf(
                "sign.action_sign_request_print_logs",
                self.ids,
                data={
                    "format_date": format_date,
                    "company_id": self.communication_company_id,
                },
            )
        )
        return self.env["ir.attachment"].create(
            {
                "name": f"Certificate of completion - {time.strftime('%Y-%m-%d - %H:%M:%S')}.pdf",
                "raw": pdf_content,
                "type": "binary",
                "res_model": self._name,
                "res_id": self.id,
            }
        )

    def _attach_completed_documents(self, doc_attachment, log_attachment):
        self.completed_document_attachment_ids = [
            Command.set([doc_attachment.id, log_attachment.id])
        ]


class SignRequestItem(models.Model):
    _inherit = "sign.request.item"

    def _get_user_signature_asset(self, asset_type):
        self.ensure_one()
        sign_user = self.partner_id.user_ids[:1]
        if sign_user and asset_type in ["stamp_sign_stamp", "stamp_sign_stamp_frame"]:
            return sign_user[asset_type]
        return False
