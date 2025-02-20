# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request

class PropertyController(http.Controller):

    @http.route(['/property', '/property/page/<int:page>'], type="http", auth="public", website=True)
    def property(self, page=1):
        properties = request.env['estate.property']
        properties_count = properties.search_count([('status', 'not in', ['sold', 'cancelled'])])
        pager = request.website.pager(
            url='/property',
            total=properties_count,
            page=page,
            step=4
        )
        properties = properties.search([('status', 'not in', ['sold', 'cancelled'])], offset=(page - 1)* 4, limit=4)
        return request.render("estate.property_page", {
            'properties': properties,
            'pager': pager
        })
