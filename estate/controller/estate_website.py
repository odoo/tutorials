from odoo import http
from odoo.http import request

class EstateWebsite(http.Controller):
    @http.route(['/properties'], type='http', auth="public", website=True, methods=['GET'])
    def list_properties(self):
        properties = request.env['estate.property'].sudo().search([('is_published', '=', True), ('state', '!=', 'sold')])
        return request.render('estate.property_listing_template', {'properties': properties})

class PropertyController(http.Controller):
    @http.route('/property/details', type='http', auth='public', website=True, methods=['GET'])
    def property_details(self, property_id):
        property_obj = request.env['estate.property'].sudo().browse(int(property_id.strip()))
        if not property_obj.exists():
            return request.not_found()
        return request.render('estate.property_detail_template', {'property': property_obj})
