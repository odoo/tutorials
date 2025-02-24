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

        attachments = [
            {
                "res_id": bill.id,
                "res_model": "account.move",
                "name": "invoice.pdf",
                "datas": base64.b64encode(pdf_file.read()),
                "type": "binary",
                "mimetype": "application/pdf",
            },
            {
                "res_id": bill.id,
                "res_model": "account.move",
                "name": "invoice.xml",
                "datas": base64.b64encode(xml_file.read()),
                "type": "binary",
                "mimetype": "application/xml",
            }
        ]

        request.env["ir.attachment"].sudo().create(attachments)

        return request.render('supplier_portal.generic_message', {"message": "Document uplaoded successfully"})
