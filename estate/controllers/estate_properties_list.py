from odoo import http
from odoo.http import request

class EstatePropertyList(http.Controller):
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def property_list(self, page=1):
        Property = request.env['estate.property']
        domain = [('state', 'in', ['new', 'offer_received'])]
        properties_count = Property.search_count(domain)
        pager = request.website.pager(
            url='/properties',
            total=properties_count,
            page=page,
            step=9
        )
        properties = Property.search(domain, limit=9, offset=pager['offset'])
        return request.render('estate.properties_list', {'properties': properties, 'pager': pager})

    @http.route('/property/<int:id>', type='http', auth="public", website=True)
    def property_detail(self, id, **kwargs):
        property = request.env['estate.property'].sudo().browse(id)
        if not property:
            return request.not_found()
        return request.render('estate.property_detail', {
            'property': property,
        })
