# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from datetime import datetime


class EstatePropertyController(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], auth='public', type='http', website=True)
    def property_listing(self, page=1, **kwargs):
        """Displays a paginated list of properties."""
        domain = [('state', 'not in', ['sold', 'archived'])]
        listed_after = kwargs.get('listed_after')
        
        if listed_after:
            try:
                listed_after_date = datetime.strptime(listed_after, "%Y-%m-%d")
                domain.append(('date_availability', '>=', listed_after_date))
            except ValueError:
                pass

        properties = request.env['estate.property'].sudo().search(
            domain, limit=6, offset=(page - 1) * 6, order='date_availability desc'
        )
        
        total_properties = request.env['estate.property'].sudo().search_count(domain)

        pager = request.website.pager(
            url='/properties',
            total=total_properties,
            page=page,
            step=6,
            scope=5,
        )

        return request.render('estate.property_listing_page', {
            'properties': properties,
            'pager': pager,
        })
        
    @http.route('/property/<model("estate.property"):property>', auth='public', website=True)
    def property_details(self, property, **kwargs):
        return request.render('estate.property_detail_page', {
            'property': property
        })
