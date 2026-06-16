import base64

from odoo import http
from odoo.http import request


class SupplierPortalController(http.Controller):
    @http.route(
        "/my/supplier/upload_bill",
        type="http",
        auth="public",
        methods=["get"],
        website=True,
    )
    def supplierPortal(self):
        user = request.env.user

        return request.render(
            "account_supplier_portal.account_supplier_portal_view",
            {
                "allowed_companies": user.partner_id.parent_id,
            },
        )

    @http.route(
        "/my/supplier/upload_bill",
        type="http",
        auth="public",
        methods=["post"],
        website=True,
    )
    def submitBill(self, **kwargs):

        partner_id = int(kwargs.get("partner_id"))
        pdf_file = kwargs.get("pdf_file")
        xml_file = kwargs.get("xml_file")

        bill_vals = {
            "move_type": "in_invoice",  # Inbound Vendor Bill
            "state": "draft",
            "partner_id": partner_id,
        }
        new_bill = request.env["account.move"].sudo().create(bill_vals)

        attachments_to_create = []

        if pdf_file:
            attachments_to_create.append(
                {
                    "name": pdf_file.filename,
                    "datas": base64.b64encode(pdf_file.read()),
                    "res_model": "account.move",
                    "res_id": new_bill.id,
                }
            )

        if xml_file:
            attachments_to_create.append(
                {
                    "name": xml_file.filename,
                    "datas": base64.b64encode(xml_file.read()),
                    "res_model": "account.move",
                    "res_id": new_bill.id,
                }
            )

        if attachments_to_create:
            request.env["ir.attachment"].sudo().create(attachments_to_create)

            new_bill.sudo().message_post(
                body="Vendor Bill submitted via Supplier Portal.",
                attachment_ids=[att.id for att in new_bill.attachment_ids],
            )

        return request.redirect("/supplier-portal-bill-added")
