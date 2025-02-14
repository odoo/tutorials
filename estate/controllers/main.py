from odoo import http
from odoo.http import request

class MyController(http.Controller):
    
    @http.route('/my/custom/route', auth='public', website=True)
    def my_custom_route(self):
        return http.request.render('estate.my_template', {
            'my_variable': 'Hello, Odoo!'
        })
    
    @http.route('/api/get_data', type='json', auth='user', csrf=False)
    def api_get_data(self):
        return {
            'status': 'success',
        }


