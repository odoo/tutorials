# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.http import Controller, request, route


class EstateProperty(Controller):
    @route("/property", type="http", auth="public", website=True)
    def estate_property(self):
        properties = request.env['estate.properties'].sudo().search(
            [('state', 'in', ('new', 'offer received'))])
        return request.render("real_estate.web_template_estate_properties", {'records': properties})
