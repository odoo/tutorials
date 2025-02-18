from odoo import http
from odoo.http import request

class Estate(http.Controller):
    
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def properties(self, page=1, listed_after=None, **kwargs):
        Property = request.env['estate.property']
        domain = [('state', '!=', 'sold'), ('state', '!=', 'canceled'), ('state', '!=', 'archived')]
        
        if listed_after:
            domain.append(('create_date', '>=', listed_after))
        
        properties_count = Property.search_count(domain)
        properties = Property.search(domain, order='create_date desc', limit=6, offset=(page-1)*6)
        
        if not properties:
            return request.render('website.404')
        
        return request.render('estate.property_list', {
            'properties': properties,
            'page': page,
            'pager': request.website.pager(
                url='/properties',
                total=properties_count,
                page=page,
                step=6
            ),
            'listed_after': listed_after
        })

    @http.route(['/property/<int:property_id>'], type='http', auth='public', website=True)
    def property_details(self, property_id, **kwargs):
        property_obj = request.env['estate.property'].sudo().browse(property_id)
        if not property_obj.exists():
            return request.render('website.404')
        
        return request.render('estate.property_detail', {'property': property_obj})
