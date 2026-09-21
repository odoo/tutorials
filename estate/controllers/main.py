from odoo import http
from odoo.http import request


class EstateWebsiteController(http.Controller):
    @http.route(["/properties"], type="http", auth="public", website=True)
    def properties_list(self, sale_mode="all", min_price=None, max_price=None, **post):
        domain = [("active", "=", True)]
        if sale_mode in ["auction", "regular"]:
            domain.append(("sale_mode", "=", sale_mode))

        if min_price and min_price.isdigit():
            domain.append(("expected_price", ">=", float(min_price)))
        if max_price and max_price.isdigit():
            domain.append(("expected_price", "<=", float(max_price)))

        properties = request.env["estate.property"].search(domain)

        values = {
            "properties": properties,
            "selected_sale_mode": sale_mode,
            "min_price": min_price or "",
            "max_price": max_price or "",
        }
        return request.render("estate.properties_page_template", values)

    @http.route(
        ["/properties/<model('estate.property'):property_rec>"],
        type="http",
        auth="public",
        website=True,
    )
    def properties_detail(self, property_rec, **post):
        values = {
            "property": property_rec,
            "user_partner": request.env.user.partner_id
            if not request.env.user._is_admin()
            else False,
        }
        return request.render("estate.properties_detail_template", values)

    @http.route(
        ["/properties/<model('estate.property'):property_rec>/offer"],
        type="http",
        auth="user",
        website=True,
    )
    def create_offer_page(self, property_rec, **post):
        values = {
            "property": property_rec,
            "partner": request.env.user.partner_id,
        }
        return request.render("estate.property_create_offer_template", values)

    @http.route(
        ["/property/offer/submit"],
        type="http",
        auth="user",
        methods=["POST"],
        website=True,
    )
    def submit_offer(self, property_id, price, **post):
        property_rec = request.env["estate.property"].browse(int(property_id))
        if property_rec.exists():
            property_rec.env["estate.property.offer"].create(
                {
                    "property_id": property_rec.id,
                    "price": float(price) if price else 0.0,
                    "partner_id": request.env.user.partner_id.id,
                }
            )
        return request.redirect(
            f"/property/offer/success?property_id={property_rec.id}"
        )

    @http.route(["/property/offer/success"], type="http", auth="user", website=True)
    def offer_success(self, property_id=None, **post):
        property_rec = (
            request.env["estate.property"].browse(int(property_id))
            if property_id and property_id.isdigit()
            else False
        )
        values = {
            "property": property_rec,
        }
        return request.render("estate.property_offer_success_template", values)
