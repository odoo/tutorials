from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def property_list(self, page=1, **searches):
        Property = request.env['estate.property']
        domain = [('state', 'in', ['new', 'offer_received'])]

        properties_count = Property.search_count(domain)
        pager = request.website.pager(
            url='/properties',
            total=properties_count,
            page=page,
            step=6,
        )

        properties = Property.search(domain, limit=6, offset=pager['offset'])
        return request.render('estate.property_listing', {
            'properties': properties,
            'pager': pager,
        })

    @http.route('/property/<model("estate.property"):estate_property>', type='http', auth='public', website=True)
    def property_detail(self, estate_property, **kwargs):
        return request.render('estate.property_detail', {
            'property': estate_property,
        })
