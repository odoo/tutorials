# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request

class EstateController(http.Controller):
    
    @http.route(['/estate/properties','/estate/properties/page/<int:page>'], type='http', auth='public', methods=['GET'], csrf=False, website=True)
    def get_properties(self,page=0):
        properties = request.env['estate.property'].sudo().search([])
        total = len(properties)
        properties_per_page = 4
        pager = request.website.pager(
            url='/estate/properties',
            total=total,
            page=page,
            step = properties_per_page
        )
        offset = pager['offset']
        properties = properties[offset: offset + properties_per_page]
        return request.render('estate.properties_template', qcontext={'properties': properties, 'pager': pager})
