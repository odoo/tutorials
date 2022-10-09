from odoo import http
from odoo.http import request, route

class OwlPlayground(http.Controller):
    @http.route(['/owl_playground/playground'], type='http', auth='public')
    def show_playground(self):
        """
        Renders the owl playground page
        """
        return request.render('owl_playground.playground')



