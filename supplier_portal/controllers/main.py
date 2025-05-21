import base64
import mimetypes
from werkzeug.exceptions import NotFound

from odoo import http
from odoo.http import request


class SupplierPortal(http.Controller):

    @http.route('/supplier/portal', type='http', auth='user', website=True)
    def supplier_portal(self):
        return request.render("supplier_portal.supplier_portal_template")

    @http.route('/supplier/invoice_submit', type='http', auth='user', csrf=True, website=True)
    def upload_invoice(self, **post):

        if not post:
            raise NotFound()

        supplier = request.env.user.partner_id
        company_id = int(post.get("company_id"))
        pdf_file = post.get("pdf_invoice")
        xml_file = post.get("xml_invoice")

        if not pdf_file and not xml_file:
            return request.render('supplier_portal.supplier_invoice_upload_fail', {"message": "One file is mandatory to upload, either PDF or XML"})

        # Validate file types
        if pdf_file and not self._is_valid_file(pdf_file, "application/pdf", ".pdf"):
            return request.render('supplier_portal.supplier_invoice_upload_fail', {
                "message": "Invalid PDF file uploaded. Only .pdf files are allowed."
            })

        if xml_file and not self._is_valid_file(xml_file, ["text/xml", "application/xml"], ".xml"):
            return request.render('supplier_portal.supplier_invoice_upload_fail', {
                "message": "Invalid XML file uploaded. Only .xml files are allowed."
            })

        # create a new vendor bill with selected company
        bill = request.env["account.move"].sudo().create({
            'move_type': 'in_invoice',
            'partner_id': supplier.id,
            'company_id': company_id,
        })

        files = []
        if pdf_file:
            files.append(("invoice.pdf", pdf_file, "application/pdf"))
        if xml_file:
            files.append(("invoice.xml", xml_file, "text/xml"))

        # add attachements to the vendor bill
        for file_name, file_type, mimetype in files:
            request.env['ir.attachment'].sudo().create({
                "name": file_name,
                "type": "binary",
                "mimetype": mimetype,
                "datas": base64.b64encode(file_type.read()),
                "res_model": "account.move",
                "res_id": bill.id,
            })

        return request.render('supplier_portal.supplier_invoice_upload_success', {"message": "Document uplaoded successfully"})

    def _is_valid_file(self, file, expected_mime_types, expected_extension):
        """Validate file type based on MIME type and extension."""
        mime_type = mimetypes.guess_type(file.filename)[0]
        return mime_type in expected_mime_types and file.filename.lower().endswith(expected_extension)
