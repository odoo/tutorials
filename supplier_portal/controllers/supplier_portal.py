import base64
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError


class SupplierPortal(http.Controller):
    @http.route("/supplier/upload", type="http", auth="user", website=True)
    def supplier_portal_upload_document(self):
        return request.render("supplier_portal.supplier_portal_upload_template")

    @http.route("/supplier/portal/submit", type="http", auth="user", website=True)
    def supplier_portal_submit_document(self, **kwargs):
        """Handles supplier document upload by creating a vendor bill (`account.move`) and attaching uploaded PDF and XML files."""
        
        bills = (
            request.env["account.move"]
            .sudo().create(
                {
                    "partner_id": request.env.user.partner_id.id,
                    "move_type": "in_invoice",
                    "company_id": int(kwargs.get("company")),
                }
            )
        )
        attachments = []
        uploaded_files = request.httprequest.files.getlist("upload_file")
        for file in uploaded_files:
            file_name = file.filename
            file_extension = file_name.split(".")[-1].lower()
            if file_extension not in ["pdf", "xml"]:
                raise ValidationError("Invalid file type. Please upload only PDF or XML files.")
            mimetype = "application/pdf" if file_extension == "pdf" else "application/xml"
            attachment = request.env["ir.attachment"].sudo().create(
                {
                    "res_id": bills.id,
                    "res_model": "account.move",
                    "name": file.filename or "Uploaded PDF",
                    "datas": base64.b64encode(file.read()),
                    "mimetype": mimetype,
                    "type": "binary",
                }
            )
            attachments.append(attachment)
        
        return request.render("supplier_portal.after_submit_message_template",
            {"success_message": f"{len(attachments)} files uploaded successfully."})
