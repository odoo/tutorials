# supplier_invoice_portal/controllers/main.py
import base64

from odoo import http
from odoo.http import request


class SupplierInvoicePortal(http.Controller):

    @http.route("/my/supplier/invoice/upload", type="http", auth="user", website=True)
    def supplier_invoice_upload_form(self, **kw):
        # allow only portal users
        if not request.env.user.has_group("base.group_portal"):
            return request.redirect("/web/login")

        companies = request.env.user.company_ids.sorted(lambda c: c.name)
        return request.render("supplier_invoice_portal.supplier_invoice_upload_form", {
            "companies": companies,
            "error": kw.get("error"),
            "success": kw.get("success"),
        })

    @http.route("/my/supplier/invoice/upload/submit", type="http", auth="user", methods=["POST"], website=True, csrf=True)
    def supplier_invoice_upload_submit(self, **post):
        if not request.env.user.has_group("base.group_portal"):
            return request.redirect("/web/login")

        company_id = int(post.get("company_id") or 0)
        allowed_company_ids = request.env.user.company_ids.ids

        pdf_file = request.httprequest.files.get("pdf_file")
        xml_file = request.httprequest.files.get("xml_file")

        pdf_name = (pdf_file.filename or "").lower()
        xml_name = (xml_file.filename or "").lower()

        # validations check
        if not pdf_name.endswith(".pdf"):
            return request.redirect("/my/supplier/invoice/upload?error=PDF+must+be+.pdf+file")

        if not xml_name.endswith(".xml"):
            return request.redirect("/my/supplier/invoice/upload?error=XML+must+be+.xml+file")

        if not company_id or company_id not in allowed_company_ids:
            return request.redirect("/my/supplier/invoice/upload?error=Invalid+company+selected")

        if not pdf_file or not pdf_file.filename:
            return request.redirect("/my/supplier/invoice/upload?error=Please+upload+PDF+file")

        if not xml_file or not xml_file.filename:
            return request.redirect("/my/supplier/invoice/upload?error=Please+upload+XML+file")

        partner = request.env.user.partner_id

        # Vendor Bill draft
        bill = request.env["account.move"].sudo().create({
            "move_type": "in_invoice",
            "partner_id": partner.id,
            "company_id": company_id,
        })

        self._create_attachment(bill, pdf_file)
        self._create_attachment(bill, xml_file)

        return request.redirect("/my/supplier/invoice/upload?success=Invoice+submitted+successfully")

    def _create_attachment(self, bill, file_storage):
        content = file_storage.read() or b""
        filename = file_storage.filename

        # for preview pdf
        mimetype = getattr(file_storage, "mimetype",
                           None) or "application/octet-stream"

        request.env["ir.attachment"].sudo().create({
            "name": filename,
            "type": "binary",
            "datas": base64.b64encode(content),
            "mimetype": mimetype,
            "res_model": "account.move",
            "res_id": bill.id,
        })
