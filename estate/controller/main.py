# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request

class PropertyController(http.Controller):

    @http.route(['/property', '/property/page/<int:page>'], type="http", auth="public", website=True)
    def property(self, page=1):

        properties = request.env['estate.property']
        domain = [('status', 'not in', ['sold', 'cancelled', 'archived'])]
        properties_count = properties.search_count(domain)
        per_page = 4 
        pager = request.website.pager(
            url='/property',
            total=properties_count,
            page=page,
            step=per_page
        )
        properties = properties.search(domain, offset=(page - 1)* per_page, limit=per_page)
        return request.render("estate.property_page", {
            'properties': properties,
            'pager': pager
        })
