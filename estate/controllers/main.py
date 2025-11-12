from urllib.parse import urlencode

from odoo import http
from odoo.exceptions import UserError
from odoo.http import request,route

class MyController(http.Controller):
    
    @route('/estate/property', auth='public', website=True)
    def my_custom_route(self):
        properties = request.env['estate.property'].sudo().search([])
        
        return request.render('estate.property_list_view', {
            'properties': properties
        })

    @route('/estate/property/<int:property_id>', type='http', auth="public", website=True)
    def property_details(self, property_id):
        property = request.env['estate.property'].sudo().browse(property_id)
        if not property.exists():
            return request.not_found()

        return request.render('estate.property_detail_page', {
            'property': property
        })

    @route('/estate/property/<int:property_id>/sold', type='http', auth="public", website=True)
    def mark_as_sold(self, property_id):
        property = request.env['estate.property'].sudo().browse(property_id)
        if property.exists():
            try:
                property.sold_property()
            except UserError as e:
                query_params = urlencode({'error_message': e})
                return request.redirect('/estate/property/%d?%s' % (property_id, query_params))
        return request.redirect('/estate/property/%d' % property_id)

    @route('/estate/property/<int:property_id>/cancelled', type='http', auth="public", website=True)
    def mark_as_cancelled(self, property_id):
        property = request.env['estate.property'].sudo().browse(property_id)
        if property.exists():
            try:
                property.cancel_property()
            except UserError as e:
                query_params = urlencode({'error_message': e})
                return request.redirect('/estate/property/%d?%s' % (property_id, query_params))
        return request.redirect('/estate/property/%d' % property_id)

    @route('/jjj', auth='public', website=True)
    def my_data(self, **kwargs):
        return "Hello!!"
    
    @route('/my_json', auth='public',type='json', website=True, method=['POST'])
    def my_js(self, **kwargs):
        return({
            "name": "mayur"
        })        
    