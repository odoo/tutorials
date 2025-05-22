from odoo import http
from odoo.http import request


class OwlPlayground(http.Controller):
    @http.route(["/awesome_owl"], type="http", auth="public")
    def show_playground(self):
        """Playground page"""
        return request.render("awesome_owl.playground")
