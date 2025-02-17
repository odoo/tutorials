from odoo import http
from odoo.http import request,route

class MyController(http.Controller):
    
    @route('/my/custom/route', auth='public', website=True)
    def my_custom_route(self):
        properties = request.env['estate.property'].sudo().search([])
        
        return http.request.render('estate.property_list_view', {
            'properties': properties
        })

    @route('/jjj', auth='public', website=True)
    def my_data(self, **kwargs):
        return "Hello!!"
    
    @route('/my_json', auth='public',type='json', website=True, method=['POST'])
    def my_js(self, **kwargs):
        return({
            "name": "mayur"
        })
        
    