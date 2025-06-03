from odoo import http
from odoo.http import request, route


class OwlPlayground(http.Controller):
    @http.route(["/awesome_owl/counter"], type="http", auth="public")
    def show_playground(self):
        """
        Renders the owl playground page
        """
        return request.render("awesome_owl.playground")

    @http.route(["/awesome_owl/todos"], type="http", auth="public")
    def show_todos(self):
        """
        Renders the owl todolist page
        """
        return request.render("awesome_owl.todolist")
