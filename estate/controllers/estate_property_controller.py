from odoo import http, _
from odoo.http import request

class EstatePropertyController(http.Controller):
    
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth="public", website=True)
    def list_properties(self, page=1, **kwargs):
        Properties = request.env['estate.property']
        
        domain = [('state', 'in', ['new', 'offer_received'])]
        properties_count = Properties.search_count(domain)
        
        per_page = 6
        offset = (page - 1) * per_page
        
        properties = Properties.search(domain, limit=per_page, offset=offset)

        values = {
            'properties': properties,
            'page': page,
            'total_pages': (properties_count + per_page - 1) // per_page,
        }

        return request.render('estate.property_list_template', values)
    
    
    @http.route('/property/<int:property_id>', type="http", auth="public", website=True)
    def property_details(self, property_id, **kwargs):
        property = request.env['estate.property'].sudo().browse(property_id)
        values = {
            "property":property
        }
        return request.render('estate.property_detail_template', values)
