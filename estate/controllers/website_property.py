# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request

class EstateWebsiteController(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def list_properties(self, page=1, **kwargs):
        Property = request.env['estate.property'].sudo()
        items_per_page = 6

        total_properties = Property.search_count([])
        pager = request.website.pager(
            url='/properties',
            total=total_properties,
            page=page,
            step=items_per_page
        )

        properties = Property.search([], limit=items_per_page, offset=(page - 1) * items_per_page)

        return request.render('estate.property_listing_template', {
            'properties': properties,
            'pager': pager
        })

    @http.route('/property/<model("estate.property"):property>', auth='public', website=True)
    def property_details(self, property, **kwargs):
        return request.render('estate.property_list_detail_page', {
            'property': property
        })
