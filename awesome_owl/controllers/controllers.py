# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details

from odoo import http
from odoo.http import request, route


class OwlPlayground(http.Controller):
    @http.route(['/awesome_owl'], type='http', auth='public')
    def show_playground(self):
        """
        Renders the owl playground page
        """
        return request.render('awesome_owl.playground')
