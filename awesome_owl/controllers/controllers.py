from odoo import http
from odoo.http import request, route

class OwlPlayground(http.Controller):
    @route(['/awesome_owl'], type='http', auth='public')
    def show_playground(self):
        """
        Renders the owl playground page
        """
        return request.render('awesome_owl.playground')

    @route(['/awesome_owl/todos'], type='http', auth='public')
    def show_todos(self):
        """
        Renders the todo lists
        """
        return request.render('awesome_owl.todolist')
