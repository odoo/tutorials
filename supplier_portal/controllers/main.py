import base64
from odoo import http
from odoo.http import request


class SupplierPortal(http.Controller):

    @http.route('/supplier_portal', type='http', auth='user', website=True)
    def supplier_portal(self):
        return request.render('supplier_portal.supplier_portal_template')

    @http.route('/supplier_portal/submit', type='http', auth='user', website=True)
    def supplier_portal_submit(self, company, pdf_file, xml_file, **kwargs):
        # Ensure company_id is valid
        company_id = int(company)

        # Create supplier bill (Vendor Bill)
        bill = request.env['account.move'].sudo().create({
            "move_type": "in_invoice",
            "partner_id": request.env.user.partner_id.id,
            "company_id": company_id,
        })

        # List of files with their corresponding names and MIME types
        files = [
            ("invoice.pdf", pdf_file, "application/pdf"),
            ("invoice.xml", xml_file, "application/xml"),
        ]

        attachments = [{
                "res_id": bill.id,
                "res_model": "account.move",
                "name": file_name,
                "datas": base64.b64encode(file_obj.read()),
                "type": "binary",
                "mimetype": mime_type,
            } for file_name, file_obj, mime_type in files
        ]

        request.env["ir.attachment"].sudo().create(attachments)

        return request.render('supplier_portal.generic_message', {"message": "Document uplaoded successfully"})
