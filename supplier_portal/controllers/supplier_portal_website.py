from datetime import datetime
import base64

from odoo import http
from odoo.http import request


class SupplierPortal(http.Controller):
    @http.route(["/supplier/upload"], auth="user", type="http", website=True)
    def supplier_login(self):
        companies = request.env.user.company_ids
        return request.render("supplier_portal.supplier_upload_page", {"companies": companies})

    @http.route(["/supplier/submit"], auth="user", type="http", methods=["POST"], website=True)
    def supplier_invoice_submit(self, **post):
        try:
            supplier = request.env.user.partner_id
            company_id = int(post.get("company"))
            pdf_invoice = post.get("pdf_invoice")
            xml_invoice = post.get("xml_invoice")
            
            # Create Vendor Bill
            bill_vals = {
                "partner_id": supplier.id,
                "move_type": "in_invoice",
                "company_id": company_id,
                "invoice_date": datetime.today(),
                "state": "draft",
            }
        
            bill = request.env["account.move"].sudo().create(bill_vals)

            for file in [pdf_invoice, xml_invoice]:
                request.env["ir.attachment"].sudo().create(
                    {
                        "name": file.filename,
                        "res_model": "account.move",
                        "res_id": bill.id,
                        "type": "binary",
                        "datas": base64.b64encode(file.read()),
                        "mimetype": file.content_type,
                    }
                )
            return request.redirect("/supplier/upload?success=1")

        except Exception as e:
            return request.redirect(f"/supplier/upload?error={str(e)}")
