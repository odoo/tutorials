from odoo import http
from odoo.http import request
import base64
from odoo.exceptions import UserError


class SupplierPortal(http.Controller):
    @http.route(["/upload-invoice"], type="http", auth="user", website=True)
    def supplier_upload_page(self, **kwargs):
        user = request.env.user
        if not user.has_group("supplier_portal.group_supplier_portal"):
            raise UserError("Only Supplier Group Users allowed!")

        companies = (
            request.env["res.company"].sudo().search([("user_ids", "in", [user.id])])
        )

        return request.render(
            "supplier_portal.upload_invoice_template",
            {
                "companies": companies,
            },
        )

    @http.route(
        ["/submit-invoice"],
        type="http",
        auth="user",
        methods=["POST"],
        csrf=True,
        website=True,
    )
    def submit_invoice(self, **post):
        pdf_file = post.get("pdf_file")
        xml_file = post.get("xml_file")
        company_id = int(post.get("company_id"))

        pdf_content = pdf_file.read() if pdf_file else b""
        xml_content = xml_file.read() if xml_file else b""

        journal = (
            request.env["account.journal"]
            .sudo()
            .search(
                [("type", "=", "purchase"), ("company_id", "=", company_id)], limit=1
            )
        )

        if not journal:
            company = request.env["res.company"].sudo().browse(company_id)
            raise UserError(f"No journal found for company: {company.name}")

        move_vals = {
            "move_type": "in_invoice",
            "partner_id": request.env.user.id,
            "state": "draft",
            "company_id": company_id,
            "journal_id": journal.id,
        }

        move = request.env["account.move"].sudo().create(move_vals)

        if pdf_content:
            request.env["ir.attachment"].sudo().create(
                {
                    "name": pdf_file.filename,
                    "type": "binary",
                    "datas": base64.b64encode(pdf_content),
                    "res_model": "account.move",
                    "res_id": move.id,
                    "mimetype": "application/pdf",
                }
            )
        if xml_content:
            request.env["ir.attachment"].sudo().create(
                {
                    "name": xml_file.filename,
                    "type": "binary",
                    "datas": base64.b64encode(xml_content),
                    "res_model": "account.move",
                    "res_id": move.id,
                    "mimetype": "text/xml",
                }
            )

        return request.redirect("/upload-invoice?success=1")
