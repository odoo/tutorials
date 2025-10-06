# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request


class PropertyController(http.Controller):

    @http.route('/properties', type='http', auth='public', website=True)
    def list_properties(self, **kwargs):
        properties = request.env['estate.property'].sudo().search([])
        return request.render('estate.property_listing_template', {'properties': properties})
