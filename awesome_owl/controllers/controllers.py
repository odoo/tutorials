from odoo import http
from odoo.http import request, route

class OwlPlayground(http.Controller):
    @http.route(['/awesome_owl'], type='http', auth='public')
    def show_playground(self):
        return request.render('awesome_owl.playground')

    # @http.route(['/card'], type='http', auth='public')
    # def show_card(self):
    #     return request.render('awesome_owl.card')