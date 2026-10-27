from odoo import http
from odoo.http import request


class OwlPlayground(http.Controller):
    @http.route(['/awesome_owl'], type='http', auth='public')
    def show_playground(self):
        """
        Renders the owl playground page
        """
        return request.render('awesome_owl.playground')

    @http.route(['/awesome_owl/todo'], type='http', auth='public')
    def show_todo(self):
        """Renders the Todo List page."""
        return request.render('awesome_owl.playground')
