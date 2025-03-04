# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.estate.controllers import controllers
from odoo.http import route, request


class EstatePropertyOffer(controllers.EstateProperty):
    @route("/property", type="http", auth="public", website=True)
    def estate_property(self, **kwargs):
        property_type = kwargs.get("sell_type")
        domain = [('state', 'in', ('new', 'offer_received'))]

        if property_type:
            domain.append(('sale_type', '=', property_type))

        properties = request.env['estate.property'].sudo().search(domain)

        return request.render("estate.template_property_list_website_view", {'records': properties})
