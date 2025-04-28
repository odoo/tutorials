# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.http import request


class PortalEstate(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "offers_count" in counters:
            values["offers_count"] = request.env["estate.property.offer"].sudo().search_count(
                [("partner_id", "=", request.env.user.partner_id.id)], limit=1
            )
        return values

    @http.route(['/my/property-offers'], type='http', auth="user", website=True)
    def portal_my_offers(self):
        offers = request.env["estate.property.offer"].sudo().search(
            [("partner_id", "=", request.env.user.partner_id.id)])
        values = {}
        values.update({"offers": offers, "page_name": "offers"})
        return request.render("estate.portal_my_offers", values)
