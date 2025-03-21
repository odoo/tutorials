from odoo import http
from odoo.http import request

class PropertyController(http.Controller):

    @http.route('/properties', auth='public', website=True)
    def property_page(self, page=1):
        page = int(page)
        per_page = 3  
        total_properties = request.env['estate.property'].sudo().search_count([])
        
        properties = request.env['estate.property'].sudo().search([], offset=(page-1)*per_page, limit=per_page)

        return request.render('real_estate.property_template', {
            'properties': properties,
            'page': page,
            'total_pages': (total_properties // per_page) + (1 if total_properties % per_page else 0)
        })


    @http.route('/property/<int:property_id>', auth='public', website=True)
    def property_detail(self, property_id):
        property_obj = request.env['estate.property'].sudo().browse(property_id)
        
        if not property_obj.exists():
            return request.render("website.404") 

        return request.render("real_estate.estate_property_detailed", {
            'property': property_obj
        })
