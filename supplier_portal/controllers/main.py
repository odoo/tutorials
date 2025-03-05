import base64
import mimetypes

from odoo import http
from odoo.http import request


class SupplierPortalController(http.Controller):
    
    @http.route("/supplier/upload", type="http", auth="user", website=True)
    def upload_bill(self):
        return request.render("supplier_portal.upload_portal_template")

    @http.route("/supplier/upload/bills", type="http", auth="user", methods=['POST'], website=True, csrf=True)
    def handle_file_upload(self, **vals):
        try:
            company_id = int(vals.get("company"))
            bill_xml = vals.get("bill-type-xml")
            bill_pdf = vals.get("bill-type-pdf")
                
            if not bill_xml and not bill_pdf:
                return self._acknowledge_supplier("danger", "Error", "No bill was uploaded")

            if bill_xml and not self._is_valid_file(bill_xml, ".xml", ["application/xml", "text/xml"]):
                return self._acknowledge_supplier("danger", "Error", "Invalid file provided for XML bill.")

            if bill_pdf and not self._is_valid_file(bill_pdf, ".pdf", ["application/pdf"]):
                return self._acknowledge_supplier("danger", "Error", "Invalid file provided for PDF bill.")

            account_move = request.env["account.move"].sudo().create({
                "move_type": "in_invoice",
                "company_id": company_id,
                "partner_id": request.env.user.partner_id.id,
            })

            bills = []
            
            if bill_xml:
                bills.append(bill_xml)
            if bill_pdf:
                bills.append(bill_pdf)

            request.env["ir.attachment"].sudo().create([
                {
                    "name": bill.filename,
                    "datas": base64.b64encode(bill.read()),
                    "res_model": "account.move",
                    "res_id": account_move.id,
                    "mimetype": bill.content_type,
                } for bill in bills
            ])

            return self._acknowledge_supplier("success", "Success", "Bill uploaded successfully")
        except Exception as err:
            return self._acknowledge_supplier("danger", "Error", err)

    def _acknowledge_supplier(self, message_type, message_title, message):
        return request.render("supplier_portal.message_template", {
            "message_type": message_type,
            "message_title": message_title,
            "message": message,
        })

    def _is_valid_file(self, file, expected_file_extension, expected_mimetypes):
        file_mimetype, n = mimetypes.guess_type(file.filename)
        return file.filename.endswith(expected_file_extension) and file_mimetype in expected_mimetypes
