import base64
from werkzeug.exceptions import NotFound
from odoo import http
from odoo.http import request

class SupplierPortal(http.Controller):

    @http.route('/supplier_portal', type='http', auth='user', website=True)
    def supplier_portal(self):
        return request.render("website_supplier_portal.website_supplier_portal")

    @http.route('/supplier_portal/invoice_submit', type='http', auth='user', csrf=True, website=True)
    def upload_invoice(self, **post):
        if not post:
            raise NotFound()
        supplier = request.env.user.partner_id
        company_id = int(post.get("company_id"))
        pdf_file, xml_file = post.get("pdf_invoice"), post.get("xml_invoice")
        if not (pdf_file or xml_file):
            return self._render_fail("One file is mandatory to upload, either PDF or XML")
        bill = request.env["account.move"].sudo().create({
            "move_type": "in_invoice",
            "partner_id": supplier.id,
            "company_id": company_id,
        })
        for file, mimetype in [(pdf_file, "application/pdf"), (xml_file, "application/xml")]:
            if file:
                request.env["ir.attachment"].sudo().create({
                    "name": file.filename,
                    "type": "binary",
                    "mimetype": mimetype,
                    "datas": base64.b64encode(file.read()),
                    "res_model": "account.move",
                    "res_id": bill.id,
                })
        return request.render('website_supplier_portal.supplier_invoice_upload_success',
                              {"message": "Document uploaded successfully"})

    def _render_fail(self, message):
        return request.render('website_supplier_portal.supplier_invoice_upload_fail', {"message": message})
