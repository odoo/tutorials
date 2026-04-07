from odoo import fields
from odoo.http import Controller, request, route


class EstateAuctionWebsite(Controller):
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

        if (property_obj.sale_type != "auction" or property_obj.state != "auction"):
            return request.redirect(property_url)
        if property_obj.auction_end_time and property_obj.auction_end_time <= fields.Datetime.now():
            return request.redirect(property_url)

        bid_amount = float(amount)

        request.env["estate.property.offer"].sudo().create(
            {
                "property_id": property_obj.id,
                "partner_id": request.env.user.partner_id.id,
                "price": bid_amount,
            },
        )

        return request.redirect(f"{property_url}/bid/success")

    @route(
        "/properties/<int:property_id>/bid/success",
        type="http",
        auth="user",
        website=True,
    )
    def auction_bid_success(self, property_id, **kwargs):
        property_obj = request.env["estate.property"].sudo().browse(property_id)
        return request.render("estate_auction.website_auction_bid_success", {"property": property_obj})
