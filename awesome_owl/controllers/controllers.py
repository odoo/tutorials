from odoo import http
from odoo.http import request, route


class OwlPlayground(http.Controller):
    @http.route(['/awesome_owl/playground'], type='http', auth='user')
    def show_playground(self):
        """
        Renders the owl playground page
        """
        return request.render('awesome_owl.playground_template')
