from odoo import http
from odoo.http import request, route

class OwlPlayground(http.Controller):
    @http.route(['/c'], type='http', auth='public')
    def show_playground(self):
        """
        Renders the owl playground page
        """
        return request.render('awesome_owl.playground')

    @http.route(['/todo_list'], type='http', auth='public')
    def show_todo_list(self):
        """
        Renders the owl playground page
        """
        return request.render('awesome_owl.todo_list')