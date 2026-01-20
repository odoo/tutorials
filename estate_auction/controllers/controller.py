# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _
from odoo.http import Controller, request, route


class EstatePropertyOffer(Controller):
    @route("/create", type="http", auth="public", website=True, methods=['POST'])
    def create_offer(self, **post):
        try:
            offer_price = float(post.get("offer_price", 0))
            partner_id = int(post.get("partner_id", 0))
            property_id = int(post.get("property_id", 0))

            if not partner_id or not property_id or offer_price <= 0:
                return request.render("estate_auction.template_estate_auction_property_offer_error", {
                    "error_title": _("Warning"),
                    "error_message": _("Missing Required Fields"),
                })

            property_record = request.env["estate.property"].sudo().browse(
                property_id)

            if property_record.expected_price > offer_price:
                return request.render("estate_auction.template_estate_auction_property_offer_error", {
                    "error_title": _("Warning"),
                    "error_message": _("Offer price must be greater or equal to %s") % property_record.expected_price,
                })

            request.env["estate.property.offer"].create({
                "partner_id": partner_id,
                "property_id": property_id,
                "price": offer_price,
                "offer_type": "auction"
            })

            return request.render("estate_auction.template_estate_auction_property_offer_success", {
                "property": property_record
            })

        except Exception as err:
            return request.render("estate_auction.template_estate_auction_property_offer_error", {
                "error_title": _("Error"),
                "error_message": _("An Error Occurred: %s") % str(err),
            })
