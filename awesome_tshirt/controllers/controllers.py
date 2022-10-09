# -*- coding: utf-8 -*-

import logging
import random

from odoo import http
from odoo.http import request

logger = logging.getLogger(__name__)


class AwesomeTshirt(http.Controller):
    @http.route(['/awesome_tshirt/order'], type='http', auth='public')
    def make_order(self):
        """
        Renders the public page to make orders
        """
        return request.render('awesome_tshirt.order_public_page')

    @http.route(['/awesome_tshirt/validate_order'], type='http', auth="public", methods=['POST'], website=True)
    def validate_order(self, name, email, address, quantity, size, url):
        """
        Creates an order (and optionnaly a partner) with the given data
        """
        Partner = request.env['res.partner'].sudo()
        customer = Partner.search([('email', '=', email)], limit=1)
        if not customer:
            customer = Partner.create({
                'street': address,
                'email': email,
                'name': name,
            })
        request.env['awesome_tshirt.order'].create({
            'customer_id': customer.id,
            'quantity': quantity,
            'size': size,
            'image_url': url,
        })
        return request.render('awesome_tshirt.thank_you')

    @http.route('/awesome_tshirt/statistics', type='json', auth='user')
    def get_statistics(self):
        return http.request.env['awesome_tshirt.order'].get_statistics()
