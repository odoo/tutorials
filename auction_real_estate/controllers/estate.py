from odoo import http
from odoo.http import request
from odoo.addons.estate.controllers.estate import EstatePropertyController


class EstatePropertyController(EstatePropertyController):
    @http.route(["/properties", "/properties/page/<int:page>"], type="http", auth="public", website=True)
    def properties(self, page=1, **kwargs):
        res = super().properties(page=page, **kwargs)
        sale_mode = kwargs.get("sale_mode")
        if sale_mode == "auction":
            domain = [("sale_mode", "ilike", sale_mode)]
            properties = res.qcontext["properties"].search(domain)
            res.qcontext["properties"] = properties
        return res

    @http.route(["/properties/<int:property_id>/offer/new"], type="http", auth="user", website=True)
    def create_offer(self, property_id):
        property = request.env["estate.property"].browse(property_id)
        user = request.env.user
        if not property.exists():
            return request.redirect("/properties")
        return request.render(
            "auction_real_estate.estate_property_offer_template",
            {"property": property, "user": user},
        )

    @http.route(["/properties/<int:property_id>/offer"], type="http", auth="user", website=True, csrf=False)
    def submit_offer(self, property_id, amount):
        property = request.env["estate.property"].browse(property_id)
        if not property.exists():
            return request.redirect("/properties")
        user = request.env.user
        success = False
        if float(amount) < property.expected_price:
            return request.render(
                "auction_real_estate.estate_property_offer_status_template",
                {"success": success},
            )
        request.env["estate.property.offer"].sudo().create(
            {"price": float(amount), "partner_id": user.id, "property_id": property.id}
        )
        success = True
        return request.render(
            "auction_real_estate.estate_property_offer_status_template",
            {"success": success},
        )
