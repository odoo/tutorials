from odoo import http
from odoo.http import request, route

class OwlPlayground(http.Controller):
    @http.route(['/portal'], type='http', auth='public')
    def show_playground(self):
        """
        Renders the portal page
        """
        return request.render('myportal.playground',{})