from odoo import http
from odoo.http import request

class MyController(http.Controller):
    
    @http.route('/params', auth='public', methods=['GET'], csrf=False)
    def get_params(self):
        """
        Handles GET and POST requests to retrieve and display request parameters.
        """
        params = request.get_http_params()  # Extract query string and form data
        return request.make_response(f"Request Parameters: {params}")