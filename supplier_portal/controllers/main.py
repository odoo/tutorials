import base64
import mimetypes

from odoo import http
from odoo.http import request
from odoo.exceptions import UserError


class SupplierPortalController(http.Controller):
    @http.route('/suppliers', type='http', auth='user', website=True)
    def supplier_portal(self):
        return request.render('supplier_portal.supplier_portal_form_template')

    @http.route('/suppliers/submit', type='http', auth='user', website=True)
    def supplier_portal_submission(self, **post):
        partner = request.env.user.partner_id
        company_id = int(post.get('company_id'))
        pdf_file = post.get('pdf_file')  
        xml_file = post.get('xml_file')

        if pdf_file and not self._is_file_valid(pdf_file, "application/pdf", ".pdf"):
            return request.render('supplier_portal.response_page', {"message_type": "fail"})
        
        if xml_file and not self._is_file_valid(xml_file, ["text/xml", "application/xml"], ".xml"):
            return request.render('supplier_portal.response_page', {"message_type": "fail"})

        bill = request.env["account.move"].sudo().create({
            'move_type':'in_invoice',
            'partner_id': partner.id,
            'company_id': company_id
        })

        files = []
        if pdf_file:
            files.append((pdf_file.filename, pdf_file, "application/pdf"))
        if xml_file:
            files.append((xml_file.filename, xml_file, "text/xml"))

        request.env['ir.attachment'].sudo().create([{
            "name": file_name,
            "type": "binary",
            "mimetype": mimetype,
            "datas": base64.b64encode(file.read()),
            "res_model": "account.move",
            "res_id": bill.id,
        } for file_name, file, mimetype in files])
        
        return request.render('supplier_portal.response_page', {"message_type":"success"})

    def _is_file_valid(self, file, expected_mime_types, expected_extension):
        mime_type, _ = mimetypes.guess_type(file.filename)
        return mime_type in expected_mime_types and file.filename.lower().endswith(expected_extension)
