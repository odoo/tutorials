from odoo import http
from odoo.http import request


class OwlPlayground(http.Controller):

    @http.route('/awesome_owl', type='http', auth='public', website=True)
    def playground(self):
        return request.render('awesome_owl.playground_page')
