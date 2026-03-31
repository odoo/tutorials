from odoo import http
from odoo.http import request


class EstateWebsite(http.Controller):
    _property_per_page = 8

    @http.route(
        ["/properties", "/properties/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def website_properties(self, page=1, search="", **kwargs):

        sale_type = kwargs.get("sale_type")
        website = request.website
        domain = [("state", "in", ("new", "offer_received"))]

        if sale_type:
            domain.append(("sale_type", "=", sale_type))

        if search:
            domain.append(("name", "ilike", search))

        found_properties = request.env["estate.property"].sudo().search(domain)
        total = len(found_properties)

        pager = website.pager(
            url=request.httprequest.path.partition("/page/")[0],
            total=total,
            page=page,
            step=self._property_per_page,
            url_args={"search": search},
        )
        offset = pager["offset"]
        properties_to_display = found_properties[
            offset : offset + self._property_per_page
        ]

        return request.render(
            "estate_auction.website_estate_properties",
            {
                "properties": properties_to_display,
                "pager": pager,
                "sale_type": sale_type,
            },
        )

    @http.route(
        "/properties/<int:property_id>", type="http", auth="public", website=True
    )
    def property_detail(self, property_id, **kwargs):
        property = request.env["estate.property"].sudo().browse(property_id)

        return request.render(
            "estate_auction.property_detail_template", {"property": property}
        )

    @http.route(
        "/property/make_offer", type="http", methods=["POST"], auth="user", website=True
    )
    def make_offer(self, **post):
        property_id = int(post.get("property_id"))
        property = request.env["estate.property"].sudo().browse(property_id)
        price = float(post.get("price"))

        if property.sale_type != "auction" or property.auction_state != "running":
            return request.redirect("/properties")

        if property.remaining_time == "Auction is Ended":
            return request.redirect(f"/property/{property_id}/offer/error")

        request.env["estate.property.offer"].create(
            {
                "property_id": property_id,
                "price": price,
                "partner_id": self.env.user.partner_id.id,
            }
        )
        return request.redirect(f"/property/{property_id}/offer/success")

    @http.route(
        "/property/<int:property_id>/offer/success",
        type="http",
        auth="user",
        website=True,
    )
    def offer_success(self, **kwargs):

        return request.render(
            "estate_auction.offer_success_template",
        )

    @http.route(
        "/property/<int:property_id>/offer/error",
        type="http",
        auth="user",
        website=True,
    )
    def auction_error(self, property_id, **kwargs):
        property = request.env["estate.property"].sudo().browse(property_id)
        return request.render(
            "estate_auction.auction_error_template", {"property": property}
        )
