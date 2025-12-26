import base64
from odoo import http
from odoo.http import request

class SupplierPortal(http.Controller):

    @http.route(["/my/upload_documents"], type="http", auth="user", website=True)
    def upload_documents(self, **kwargs):
        return request.render(
            "supplier_portal.supplier_portal_template",
        )

    @http.route(["/my/upload_documents/submit"], type="http", auth="user", website=True)
    def upload_documents_submit(self, **kwargs):
        documents = (
            request.env["account.move"]
            .sudo()
            .create(
                {
                    "move_type": "in_invoice",
                    "partner_id": request.env.user.partner_id.id,
                    "company_id": int(kwargs.get("company")),
                }
            )
        )

        request.env["ir.attachment"].sudo().create(
            {
                "res_id": documents.id,
                "res_model": "account.move",
                "name": "Invoice PDF",
                "datas": base64.b64encode(kwargs.get("upload_pdf").read()),
                "type": "binary",
                "mimetype": "application/pdf",
            }
        )

        request.env["ir.attachment"].sudo().create(
            {
                "res_id": documents.id,
                "res_model": "account.move",
                "name": "Invoice XML",
                "datas": base64.b64encode(kwargs.get("upload_xml").read()),
                "type": "binary",
                "mimetype": "application/xml",
            }
        )

        return request.render(
            "supplier_portal.generic_message_template",
            {"success_message": "Documents uploaded successfully."},
        )
