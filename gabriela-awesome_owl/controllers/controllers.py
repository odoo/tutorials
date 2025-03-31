from odoo import http
from odoo.http import request, route

class OwlPlayground(http.Controller):
    @http.route(['/gabriela-awesome_owl'], type='http', auth='public')
    def show_playground(self):
        """
        Renders the owl playground page
        """
        return request.render('gabriela-awesome_owl.playground')
