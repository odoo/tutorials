from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def list_properties(self, page=1, **kwargs):
        Property = request.env['estate.property']
        domain = [('state', 'not in', ['sold', 'cancelled']), ('active', '=', True)]
        properties_count = Property.search_count(domain)
        pager = request.website.pager(
            url='/properties',
            total=properties_count,
            page=page,
            step=6
        )
        properties = Property.search(domain, limit=6, offset=pager['offset'])
        values = {
            'properties': properties,
            'pager': pager,
        }
        return request.render('estate.property_list_template', values)

    @http.route('/property/<model("estate.property"):property_detail>', type='http', auth='public', website=True)
    def view_property(self, property_detail, **kwargs):
        return request.render('estate.property_detail_template', {'property': property_detail})
