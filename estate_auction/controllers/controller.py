# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.http import Controller, request, route


class EstatePropertyOffer(Controller):
    @route("/create", type="http", auth="public", website=True, methods=['POST'])
    def create_offer(self, **post):
        offer_price = post.get("offer_price")
        partner_id = post.get("partner_id")
        property_id = post.get("property_id")

        try:
            partner_id = int(partner_id) if partner_id else None
            property_id = int(property_id) if property_id else None
            offer_price = float(offer_price) if offer_price else None

            if not partner_id or not property_id or offer_price is None:
                return request.redirect("/error?message=Missing+Required+Fields")

            property_record = request.env["estate.property"].sudo().browse(
                property_id)

            request.env["estate.property.offer"].create({
                "partner_id": partner_id,
                "property_id": property_id,
                "price": offer_price,
                "offer_type": "auction"
            })

            return request.render("estate_auction.template_property_offer_success", {"property": property_record.name})

        except ValueError:
            return request.send("An Error Occured")
