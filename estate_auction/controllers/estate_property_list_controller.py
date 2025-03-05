# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.estate.controllers import controllers
from odoo.http import route, request
from datetime import datetime


class EstatePropertyOffer(controllers.EstateProperty):
    @route("/property", type="http", auth="public", website=True)
    def estate_property(self, **kwargs):
        sale_type = kwargs.get("sale_type")
        domain = [('state', 'in', ('new', 'offer_received'))]

        if sale_type:
            domain.append(('sale_type', '=', sale_type))

        properties = request.env['estate.property'].sudo().search(domain)

        return request.render("estate.template_property_list_website_view", {'records': properties})

    @route("/property/<int:id>", type="http", auth="public", website=True)
    def estate_property_details(self, id):
        property_details = request.env["estate.property"].sudo().browse(id)
        if property_details.exists():
            is_auction_ended = property_details.auction_end_time and property_details.auction_end_time < datetime.now()
            return request.render("estate.template_property_detail_website_view", {'property': property_details, 'is_auction_ended': is_auction_ended})
        return request.render("estate.template_property_detail_website_view")
