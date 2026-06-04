from odoo.http import request, route
from odoo import http


class SellerProductDashboard(http.Controller):
    @route(route="/my/marketplace/dashboard", type="http", website=True)
    def seller_dashboard(self, **kw):
        current_user = request.env.user.partner_id

        if not current_user:
            return request.redirect("/")

        seller_products = (
            request.env["product.template"]
            .sudo()
            .search([("seller_id", "=", current_user.id)])
        )

        values = {"seller": current_user, "products": seller_products}

        return request.render("web_sale_purchase.seller_dashboard_template", values)
