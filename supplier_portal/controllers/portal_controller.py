import base64

from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request


class SupplierPortal(CustomerPortal):
    @http.route(["/my/upload_documents"], type="http", auth="user", website=True)
    def upload_documents(self, **kwargs):
        # Ensure the user is a portal user
        if not request.env.user.has_group("base.group_portal"):
            return request.render(
                "supplier_portal.generic_message_template",
                {
                    "error_message": "You are not allowed to access this page. Only portal users are allowed."
                },
            )
        return request.render(
            "supplier_portal.supplier_portal_template",
        )

    @http.route(["/my/upload_documents/submit"], type="http", auth="user", website=True)
    def upload_documents_submit(self, **kwargs):
        if not request.env.user.has_group("base.group_portal"):
            return request.render(
                "supplier_portal.generic_message_template",
                {
                    "error_message": "You are not allowed to access this page. Only portal users are allowed."
                },
            )

        if not kwargs.get("upload_pdf") or not kwargs.get("company"):
            return request.render(
                "supplier_portal.generic_message_template",
                {
                    "error_message": "All fields are required.",
                },
            )
        bill = (
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
                "res_id": bill.id,
                "res_model": "account.move",
                "name": "Invoice PDF",
                "datas": base64.b64encode(kwargs.get("upload_pdf").read()),
                "type": "binary",
                "mimetype": "application/pdf",
            }
        )

        request.env["ir.attachment"].sudo().create(
            {
                "res_id": bill.id,
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
