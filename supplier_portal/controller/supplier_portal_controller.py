import base64 
import mimetypes 

from odoo import http
from odoo.http import request


class SupplierPortalController(http.Controller):
    @http.route('/supplier/portal', type='http', auth='user', website=True)
    def supplier_portal(self, **kwargs):
        return request.render(
            "supplier_portal.supplier_invoice_upload_form",
        )
        
    @http.route('/supplier/upload_invoice', type='http', auth='user', website=True)
    def upload_invoice(self, **post):
        company = post.get('company')
        pdf_file = post.get('pdf_file')
        xml_file = post.get('xml_file')

        if not company:
            return request.render("supplier_portal.message_template", {
                'error_message': "Please select an organization."
            })
        
        if not pdf_file and not xml_file:
            return request.render('supplier_portal.message_template', {
                "error_message": "You need to upload at least on file: PDF or XML"
            })

        if pdf_file and not self._validate_file(pdf_file, ["application/pdf"], ".pdf"):
            return request.render("supplier_portal.message_template", {
                "error_message": "The uploaded file is not a valid PDF. Please ensure the file format is .pdf."
            })

        if xml_file and not self._validate_file(xml_file, ["text/xml", "application/xml"], ".xml"):
            return request.render("supplier_portal.message_template", {
                "error_message": "The uploaded file is not a valid XML file. Please ensure the file format is .xml"
            })

        bill = request.env["account.move"].sudo().create({
            'move_type': 'in_invoice',
            'partner_id': request.env.user.partner_id.id,
            'company_id': int(company),
        })

        request.env["ir.attachment"].sudo().create(
            {
                "name": "Invoice PDF",
                "res_id": bill.id,
                "res_model": "account.move",
                "datas": base64.b64encode(pdf_file.read()),
                "type": "binary",
                "mimetype": "application/pdf",
            }
        )
        
        request.env["ir.attachment"].sudo().create(
            {
                "name": "Invoice XML",
                "res_id": bill.id,
                "res_model": "account.move",
                "datas": base64.b64encode(xml_file.read()),
                "type": "binary",
                "mimetype": "text/xml",
            }
        )
        
        return request.render("supplier_portal.message_template", {
            'success_message': "Documents uploaded successfully!"
        })

    def _validate_file(self, file, allowed_mimes, extension):
        if not file:
            return False 

        detected_mime = mimetypes.guess_type(file.filename)[0]
        file_ext = file.filename.lower().endswith(extension) 

        return detected_mime in allowed_mimes and file_ext
