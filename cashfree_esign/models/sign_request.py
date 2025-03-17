# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import io
import time

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError

from odoo import models, Command, _
from odoo.exceptions import ValidationError
from odoo.tools import format_date
from odoo.tools.misc import file_path
from odoo.tools.pdf import PdfFileReader, PdfFileWriter, PdfReadError


def _fix_image_transparency(image):
    pixels = image.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            if pixels[x, y] == (0, 0, 0, 0):
                pixels[x, y] = (255, 255, 255, 0)


class SignRequest(models.Model):
    _name = 'sign.request'
    _inherit = 'sign.request'

    def _generate_completed_document(self):
        self.ensure_one()
        super()._generate_completed_document()
        try:
            old_pdf = PdfFileReader(io.BytesIO(base64.b64decode(self.completed_document)), strict=False, overwriteWarnings=False)
            old_pdf.getNumPages()
        except (PdfReadError, Exception):
            raise ValidationError(_("ERROR: Invalid PDF file!"))

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
            width = float(abs(page.mediaBox.getWidth()))
            height = float(abs(page.mediaBox.getHeight()))
            items = itemsByPage.get(p + 1, [])
            for item in items:
                value_dict = values.get(item.id)
                if not value_dict:
                    continue
                value = value_dict['value']
                if item.type_id.item_type == "signature":
                    try:
                        if item.responsible_id.auth_method == 'aadhar_esign':
                            email = ""
                            for x in self.request_item_ids:
                                if x.role_id.id == item.responsible_id.id:
                                    email = x.partner_id.email
                                    break
                            modified_sign = self.modify_signature(value[value.find(',') + 1:], email)
                            image_reader = ImageReader(io.BytesIO(base64.b64decode(modified_sign)))
                        else:
                            image_reader = ImageReader(io.BytesIO(base64.b64decode(value[value.find(',') + 1:])))
                    except UnidentifiedImageError:
                        raise ValidationError(_("There was an issue downloading your document. Please contact an administrator."))
                    _fix_image_transparency(image_reader._image)
                    can.drawImage(image_reader, width * item.posX, height * (1 - item.posY - item.height), width * item.width, height * item.height, 'auto', True)
            can.showPage()
        can.save()
        item_pdf = PdfFileReader(packet, overwriteWarnings=False)
        new_pdf = PdfFileWriter()

        for p in range(0, old_pdf.getNumPages()):
            page = old_pdf.getPage(p)
            page.mergePage(item_pdf.getPage(p))
            new_pdf.addPage(page)
        try:
            output = io.BytesIO()
            new_pdf.write(output)
        except PdfReadError:
            raise ValidationError(_("There was an issue downloading your document. Please contact an administrator."))

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

    def modify_signature(self, signature_data, email):
        image_file = base64.b64decode(signature_data)
        image = Image.open(io.BytesIO(image_file))

        width, height = image.size
        draw = ImageDraw.Draw(image)
        font_size = int(height * 0.15)
        try:
            font_type = 'Reg'
            lato_path = f'web/static/fonts/lato/Lato-{font_type}-webfont.ttf'
            font = ImageFont.truetype(file_path(lato_path), font_size)
        except OSError:
            font = ImageFont.load_default()

        text = "Aadhar Esign by " + email
        text_color = (0, 0, 255)

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        while text_width > width - 20 and font_size > 10:
            font_size -= 2
            font_type = 'Reg'
            lato_path = f'web/static/fonts/lato/Lato-{font_type}-webfont.ttf'
            font = ImageFont.truetype(file_path(lato_path), font_size)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x, y = (width - text_width) // 2, height - text_height - 10
        draw.text((x, y), text, font=font, fill=text_color)
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
