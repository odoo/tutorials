from odoo import http
from odoo.http import request

class EstatePropertyController(http.Controller):
    
    @http.route(['/properties','/properties/<int:property_id>'], type='http', auth="public", website=True)
    def list_properties(self, property_id=None, **kwargs):
        if property_id:
            property = request.env['estate.property'].sudo().browse(property_id)
            return request.render('real_estate.property_detail_template' , {'property': property})
        properties = request.env['estate.property'].sudo().search([])
        return request.render('real_estate.website_property_template', {'properties': properties})
