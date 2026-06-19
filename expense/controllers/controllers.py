from odoo import http
from odoo.http import request, route


class OwlPlayground(http.Controller):
    @http.route(["/expense"], type="http", auth="public")
    def show_expense(self):
        return request.render("expense.Playground")
