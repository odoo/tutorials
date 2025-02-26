from odoo import http
from odoo.http import request


class PropertyWebsite(http.Controller):
    @http.route(['/properties', '/properties/page/<int:page>'], auth='public', website=True)
    def list_properties(self, page=1, **kwargs):
        Property = request.env['estate.property'].sudo()
        per_page= 6
        domain = [('status', 'not in', ['sold', 'cancelled'])]
        total_properties = Property.search_count(domain)
        properties = Property.search(domain, offset=(page-1) * per_page, limit=per_page)
        pager = request.website.pager(
            url='/properties',
            total=total_properties,
            page=page,
            step=per_page
        )
        return request.render('estate.property_listing_template', {
            'properties': properties,
            'pager': pager
        })

    @http.route(['/property/<model("estate.property"):property>'], type='http', auth="public", website=True)
    def property_details(self, property, **kwargs):
        return request.render('estate.property_details_template', {
            'property': property
        })
