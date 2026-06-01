from odoo import fields
from odoo.http import request, route
from odoo.addons.estate.controllers.main import EstateWebsite


class EstateAuctionWebsite(EstateWebsite):

    @route(
        ["/properties", "/properties/page/<int:page>"],
        type="http",
        auth="public",
        website=True
    )
    def properties(self, page=1, **kwargs):
        website = request.website
        domain = []
        selling_mode = kwargs.get("selling_mode")
        if selling_mode:
            domain.append(('selling_mode', '=', selling_mode))
        found_properties = request.env["estate.property"].sudo().search(domain)

        pager = website.pager(
            url="/properties",
            total=len(found_properties),
            page=page,
            step=self._property_per_page,
            url_args=kwargs,
        )

        offset = pager["offset"]
        properties_list = found_properties[
            offset:
            offset + self._property_per_page
        ]

        return request.render(
            "estate.estate_properties_template",
            {
                "properties": properties_list,
                "pager": pager,
                "selling_mode": selling_mode,
            }
        )

    @route(
        "/properties/<int:property_id>/bid",
        type="http",
        auth="user",
        methods=["POST"],
        website=True,
    )
    def submit_auction_bid(self, property_id, amount, **kwargs):
        property_url = f"/properties/{property_id}"
        property_obj = request.env["estate.property"].sudo().browse(property_id)
        if (property_obj.selling_mode != "auction" or property_obj.auction_state != "in_progress"):
            return request.redirect(property_url)
        if (property_obj.auction_end and property_obj.auction_end <= fields.Datetime.now()):
            return request.redirect(property_url)

        request.env["estate.property.offer"].sudo().create({
            "property_id": property_obj.id,
            "partner_id": request.env.user.partner_id.id,
            "price": float(amount),
        })

        return request.redirect(f"{property_url}/bid/success")

    @route(
        "/properties/<int:property_id>/bid/success",
        type="http",
        auth="user",
        website=True)
    def auction_bid_success(self, property_id, **kwargs):
        property_obj = request.env["estate.property"].sudo().browse(property_id)
        return request.render(
            "estate_auction.website_auction_bid_success",
            {
                "property": property_obj
            }
        )
