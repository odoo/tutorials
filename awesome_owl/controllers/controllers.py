from odoo import http
from odoo.http import request, route

class OwlPlayground(http.Controller):
    @http.route(['/awesome_owl'], type='http', auth='public', website=True)
    def show_playground(self):
        return request.render('awesome_owl.playground')
