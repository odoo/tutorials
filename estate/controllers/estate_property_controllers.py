from odoo import http
from odoo.http import request

class EstatePropertyWebsite(http.Controller):
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def property_list(self, page=1, **kwargs):
        Property = request.env['estate.property'].sudo()
        domain = [('state', 'not in', ['sold', 'cancelled']), ('active', '=', True)]
        
        properties_count = Property.search_count(domain)
        page_size = 9
        pager = request.website.pager(
            url='/properties',
            total=properties_count,
            page=page,
            step=page_size
        )
        
        properties = Property.search(domain, limit=page_size, offset=pager['offset'])
        
        return request.render('estate.property_list_template', {
            'properties': properties,
            'pager': pager
        })

    @http.route('/properties/<int:property_id>', type='http', auth='public', website=True)
    def property_detail(self, property_id, **kwargs):
        property_obj = request.env['estate.property'].sudo().browse(property_id)
        if not property_obj.exists():
            return request.not_found()
        
        return request.render('estate.property_detail_template', {
            'property': property_obj
        })