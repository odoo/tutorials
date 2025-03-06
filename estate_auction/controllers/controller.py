# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _
from odoo.http import Controller, request, route


class EstatePropertyOffer(Controller):
    @route("/create", type="http", auth="public", website=True, methods=['POST'])
    def create_offer(self, **post):
        offer_price = float(post.get("offer_price"))
        partner_id = int(post.get("partner_id"))
        property_id = int(post.get("property_id"))

        try:
            if not partner_id or not property_id or offer_price is None:
                return _("Misisng Required Fields")

            property_record = request.env["estate.property"].sudo().browse(
                property_id)
            
            if property_record.expected_price > offer_price:
                return _("offer price must be greater or eaqual to %s",property_record.expected_price)

            request.env["estate.property.offer"].create({
                "partner_id": partner_id,
                "property_id": property_id,
                "price": offer_price,
                "offer_type": "auction"
            })

            return request.render("estate_auction.template_property_offer_success", {"property": property_record.name})

        except Exception as err:
            return _("An Error Occured %s",err)
