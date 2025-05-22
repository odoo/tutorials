# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.http import request


class EstateProperty(http.Controller):
    @http.route(['/properties','/properties/page/<int:page>'], type='http', auth='public', website=True)
    def estate_property(self, page=1, listed_after=None, property_name=None):
        domain = [('state', 'in', ['new', 'offer_received', 'offer_accepted'])]
        if listed_after:
            domain.append(('create_date', '>', listed_after))
        if property_name:
            domain.append(('name', 'ilike', property_name))
        total = request.env['estate.property'].search_count(domain)
        step = 6
        offset = (page - 1) * step
        pager = portal_pager(
            url = '/properties',
            url_args = {'listed_after': listed_after, 'property_name': property_name},
            page = page,
            total = total,
            step = step,
        )
        properties = request.env['estate.property'].search(domain, limit=step, offset=offset)
        values = {
            'pager': pager,
            'properties' : properties,
            'listed_after': listed_after or '',
            'property_name': property_name or '',
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
