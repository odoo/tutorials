from odoo import http
from odoo.http import request


class EstateController(http.Controller):
    @http.route("/properties", auth="public", type="http", website=True)
    def property_list(self, **kwargs):

        sale_mode = kwargs.get("sale_mode")
        status = kwargs.get("status")
        min_price = kwargs.get("min_price")
        max_price = kwargs.get("max_price")

        domain = []

        if sale_mode:
            domain.append(("sale_mode", "=", sale_mode))

        if status:
            domain.append(("state", "=", status))

        if min_price:
            domain.append(("expected_price", ">=", float(min_price)))

        if max_price:
            domain.append(("expected_price", "<=", float(max_price)))

        properties = request.env["estate.property"].search(domain)

        return request.render(
            'estate_website_settings.property_list_template',
            {
                "properties": properties,
                "sale_mode": sale_mode,
                "status": status,
                "min_price": min_price,
                "max_price": max_price,
                "states": request.env["estate.property"]._fields["state"].selection,
            },
        )

    @http.route("/properties/<int:property_id>", auth="public", type="http", website=True)
    def property_detail(self, property_id, **kwargs):

        property_record = request.env["estate.property"].browse(property_id)

        return request.render(
            "estate_website_settings.property_detail_template",
            {
                "property": property_record
            },
        )

    @http.route("/properties/<int:property_id>/create_offer", auth="user", type="http", methods=["POST"], website=True)
    def create_offer(self, property_id, **post):

        partner = request.env.user.partner_id

        request.env["estate.property.offer"].sudo().create({
            "property_id": property_id,
            "partner_id": partner.id,
            "price": float(post.get("price")),
        })

        return request.redirect("/offer-success")

    @http.route("/offer-success", auth="user", type="http", website=True)
    def offer_success(self, **kwargs):
        return request.render("estate_website_settings.offer_success_template")
