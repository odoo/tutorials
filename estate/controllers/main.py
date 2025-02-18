# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, fields
from odoo.http import request


class PropertyController(http.Controller):
    @http.route(["/properties/page/<int:page>", "/properties", "/property"], type="http", auth="public", website=True)
    def properties(self, listed_after=None, page=1):
        limit = 6
        EstateProperty = request.env["estate.property"]
        domain = [('active', '=', True), ('state', 'in', ['new', 'offer_received'])]
        try:
            listed_after_date = fields.Date.to_date(listed_after)
            domain += [('create_date', '>=', listed_after_date)]
        except:
            listed_after = None
        property_count = EstateProperty.search_count(domain)
        pager = request.website.pager(
            url="/properties",
            url_args={'listed_after': listed_after},
            total=property_count,
            page=page,
            step=limit
        )
        property_filters = {
            'listed_after': listed_after
        }
        properties = EstateProperty.search(domain=domain, limit=limit, offset=pager["offset"])
        return request.render("estate.estate_properties_grid", {'properties': properties, 'pager': pager, 'property_filters': property_filters})

    @http.route(["/property/<model('estate.property'):property>", "/properties/<model('estate.property'):property>"], type="http", auth="public", website=True)
    def view_property(self, property):
        return request.render("estate.single_property_view", {'property': property})
