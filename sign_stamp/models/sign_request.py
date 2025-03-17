import base64
import io
import time

from PIL import UnidentifiedImageError
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth

from odoo import _, models, Command
from odoo.tools import format_date
from odoo.exceptions import UserError, ValidationError
from odoo.tools.pdf import PdfFileReader, PdfFileWriter, PdfReadError, reshape_text


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
        if self.state != 'signed':
            raise UserError(_("The completed document cannot be created because the sign request is not fully signed"))
        if not self.template_id.sign_item_ids:
            self.completed_document = self.template_id.attachment_id.datas
        else:
            try:
                old_pdf = PdfFileReader(io.BytesIO(base64.b64decode(self.template_id.attachment_id.datas)), strict=False, overwriteWarnings=False)
                old_pdf.getNumPages()
            except (TypeError, base64.binascii.Error, PdfReadError):
                raise ValidationError(_("ERROR: Invalid PDF file!"))

            isEncrypted = old_pdf.isEncrypted
            if isEncrypted and not old_pdf.decrypt(password):
                # password is not correct
                return

            font = self._get_font()
            normalFontSize = self._get_normal_font_size()

            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=self.get_page_size(old_pdf))
            itemsByPage = self.template_id._get_sign_items_by_page()
            items_ids = [id for items in itemsByPage.values() for id in items.ids]
            values_dict = self.env['sign.request.item.value']._read_group(
                [('sign_item_id', 'in', items_ids), ('sign_request_id', '=', self.id)],
                groupby=['sign_item_id'],
                aggregates=['value:array_agg', 'frame_value:array_agg', 'frame_has_hash:array_agg']
            )
            values = {
                sign_item.id: {
                    'value': values[0],
                    'frame': frame_values[0],
                    'frame_has_hash': frame_has_hashes[0],
                }
                for sign_item, values, frame_values, frame_has_hashes in values_dict
            }

            for p in range(0, old_pdf.getNumPages()):
                page = old_pdf.getPage(p)
                # Absolute values are taken as it depends on the MediaBox template PDF metadata, they may be negative
                width = float(abs(page.mediaBox.getWidth()))
                height = float(abs(page.mediaBox.getHeight()))

                # Set page orientation (either 0, 90, 180 or 270)
                rotation = page.get("/Rotate", 0)
                if rotation and isinstance(rotation, int):
                    can.rotate(rotation)
                    # Translate system so that elements are placed correctly
                    # despite of the orientation
                    if rotation == 90:
                        width, height = height, width
                        can.translate(0, -height)
                    elif rotation == 180:
                        can.translate(-width, -height)
                    elif rotation == 270:
                        width, height = height, width
                        can.translate(-width, 0)

                items = itemsByPage.get(p + 1, [])
                for item in items:
                    value_dict = values.get(item.id)
                    if not value_dict:
                        continue
                    # only get the 1st
                    value = value_dict['value']
                    frame = value_dict['frame']

                    if frame:
                        try:
                            image_reader = ImageReader(io.BytesIO(base64.b64decode(frame[frame.find(',') + 1:])))
                        except UnidentifiedImageError:
                            raise ValidationError(_(
                                    "There was an issue downloading your document. Please contact an administrator."
                                ))
                        _fix_image_transparency(image_reader._image)
                        can.drawImage(
                            image_reader,
                            width * item.posX,
                            height * (1 - item.posY - item.height),
                            width * item.width,
                            height * item.height,
                            'auto',
                            True
                        )

                    if item.type_id.item_type == "text":
                        value = reshape_text(value)
                        can.setFont(font, height * item.height * 0.8)
                        if item.alignment == "left":
                            can.drawString(width * item.posX, height * (1 - item.posY - item.height * 0.9), value)
                        elif item.alignment == "right":
                            can.drawRightString(width * (item.posX + item.width), height * (1 - item.posY - item.height * 0.9), value)
                        else:
                            can.drawCentredString(width * (item.posX + item.width / 2), height * (1 - item.posY - item.height * 0.9), value)

                    elif item.type_id.item_type == "selection":
                        content = []
                        for option in item.option_ids:
                            if option.id != int(value):
                                content.append("<strike>%s</strike>" % (option.value))
                            else:
                                content.append(option.value)
                        font_size = height * normalFontSize * 0.8
                        text = " / ".join(content)
                        string_width = stringWidth(text.replace("<strike>", "").replace("</strike>", ""), font, font_size)
                        p = Paragraph(text, ParagraphStyle(name='Selection Paragraph', fontName=font, fontSize=font_size, leading=12))
                        posX = width * (item.posX + item.width * 0.5) - string_width // 2
                        posY = height * (1 - item.posY - item.height * 0.5) - p.wrap(width, height)[1] // 2
                        p.drawOn(can, posX, posY)

                    elif item.type_id.item_type == "textarea":
                        font_size = height * normalFontSize * 0.8
                        can.setFont(font, font_size)
                        lines = value.split('\n')
                        y = (1 - item.posY)
                        for line in lines:
                            empty_space = width * item.width - can.stringWidth(line, font, font_size)
                            x_shift = 0
                            if item.alignment == 'center':
                                x_shift = empty_space / 2
                            elif item.alignment == 'right':
                                x_shift = empty_space
                            y -= normalFontSize * 0.9
                            line = reshape_text(line)
                            can.drawString(width * item.posX + x_shift, height * y, line)
                            y -= normalFontSize * 0.1

                    elif item.type_id.item_type == "checkbox":
                        can.setFont(font, height * item.height * 0.8)
                        value = 'X' if value == 'on' else ''
                        can.drawString(width * item.posX, height * (1 - item.posY - item.height * 0.9), value)
                    elif item.type_id.item_type == "radio":
                        x = width * item.posX
                        y = height * (1 - item.posY)
                        w = item.width * width
                        h = item.height * height
                        # Calculate the center of the sign item rectangle.
                        c_x = x + w * 0.5
                        c_y = y - h * 0.5
                        # Draw the outer empty circle.
                        can.circle(c_x, c_y, h * 0.5)
                        if value == "on":
                            # Draw the inner filled circle.
                            can.circle(x_cen=c_x, y_cen=c_y, r=h * 0.5 * 0.75, fill=1)
                    elif item.type_id.item_type in ["signature", "initial", "stamp"]:
                        try:
                            image_reader = ImageReader(io.BytesIO(base64.b64decode(value[value.find(',') + 1:])))
                        except UnidentifiedImageError:
                            raise ValidationError(_(
                                    "There was an issue downloading your document. Please contact an administrator."
                                ))
                        _fix_image_transparency(image_reader._image)
                        can.drawImage(
                                        image_reader,
                                        width * item.posX,
                                        height * (1 - item.posY - item.height),
                                        width * item.width,
                                        height * item.height,
                                        'auto',
                                        True
                                    )

                can.showPage()

            can.save()

            item_pdf = PdfFileReader(packet, overwriteWarnings=False)
            new_pdf = PdfFileWriter()

            for p in range(0, old_pdf.getNumPages()):
                page = old_pdf.getPage(p)
                page.mergePage(item_pdf.getPage(p))
                new_pdf.addPage(page)

            if isEncrypted:
                new_pdf.encrypt(password)

            try:
                output = io.BytesIO()
                new_pdf.write(output)
            except PdfReadError:
                raise ValidationError(_(
                        "There was an issue downloading your document. Please contact an administrator."
                    ))

            self.completed_document = base64.b64encode(output.getvalue())
            output.close()

        attachment = self.env['ir.attachment'].create({
            'name': "%s.pdf" % self.reference if self.reference.split('.')[-1] != 'pdf' else self.reference,
            'datas': self.completed_document,
            'type': 'binary',
            'res_model': self._name,
            'res_id': self.id,
        })

        public_user = self.env.ref('base.public_user', raise_if_not_found=False)
        if not public_user:
            # public user was deleted, fallback to avoid crash (info may leak)
            public_user = self.env.user
        pdf_content, __ = self.env["ir.actions.report"].with_user(public_user).sudo()._render_qweb_pdf(
            'sign.action_sign_request_print_logs',
            self.ids,
            data={'format_date': format_date, 'company_id': self.communication_company_id}
        )
        attachment_log = self.env['ir.attachment'].create({
            'name': "Certificate of completion - %s.pdf" % time.strftime('%Y-%m-%d - %H:%M:%S'),
            'raw': pdf_content,
            'type': 'binary',
            'res_model': self._name,
            'res_id': self.id,
        })
        self.completed_document_attachment_ids = [Command.set([attachment.id, attachment_log.id])]
