from odoo import http
from odoo.http import request


class SupplierPortalController(http.Controller):
    @http.route("/my/supplier/upload_bill", type="http", auth="public", website=True)
    def uploadBill(self, page=1):

        return request.render("account_supplier_portal.account_supplier_portal_view")
