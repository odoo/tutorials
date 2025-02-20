# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.http import request


class EstateProperty(http.Controller):
    @http.route(['/properties','/properties/page/<int:page>'], type='http', auth='public', website=True)
    def estate_property(self, page=1):
        domain = [('state', 'in', ['new', 'offer_received', 'offer_accepted'])]
        total = request.env['estate.property'].search_count(domain)
        step = 6
        offset = (page - 1) * step
        pager = portal_pager(
            url='/properties',
            page=page,
            total=total,
            step=step,
        )
        properties = request.env['estate.property'].search(domain, limit=step, offset=offset)
        values = {
            'pager': pager,
            'properties' : properties,
        }
        return request.render('estate.estate_property_template', values)

    @http.route(['/property/<int:property_id>'], type='http', auth='public', website=True)
    def estate_property_view(self, property_id):
        property_info = request.env['estate.property'].browse(property_id)
        if not property_info.exists():
            return request.not_found()
        values = {
            'property' : property_info
        }
        return request.render('estate.estate_property_detail_template', values)
