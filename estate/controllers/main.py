from odoo import http
from datetime import datetime

class EstateController(http.Controller):

    @http.route(
        ['/properties', '/properties/pages/<int:page>'],
        type='http',
        auth='public',
        website=True,
    )
    def properties(self, page=1, date=None, **kw):  
        domain = [('state', 'in', ['new','received'])]
        properties = http.request.env['estate.property'].search(domain)
        total_properties = len(properties)
        items_per_page = 6
        order = 'create_date desc'
        # pager
        pager = http.request.website.pager(
            url = '/properties',
            total = total_properties,
            page = page,
            step = items_per_page,
        )

        properties = http.request.env['estate.property'].search(
            domain, order=order, limit=items_per_page, offset=pager['offset']
        )

        return http.request.render(
            'estate.estate_properties_web_page',
            {'properties': properties, 'pager': pager},
        )

    @http.route('/property<int:property_id>', auth='public', website=True)
    def property_details(self, property_id, **kw):
        property = http.request.env['estate.property'].browse(property_id)
        return http.request.render(
            'estate.property_details_page',
            {'property': property}
        )
