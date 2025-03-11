# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def list_properties(self, page=1,listed_after=None, search_name=None):
        domain = [('state', 'in', ['new', 'offerreceived', 'offeraccepted'])]
        properties_per_page = 6
        if search_name:
            domain.append(('name', '=', search_name))
        if listed_after:
            try:
                date_filter = datetime.strptime(listed_after, '%Y-%m-%d')
                domain.append(('create_date', '>=', date_filter))
            except ValueError:
                pass
        total_properties = request.env['estate.property'].search_count(domain)
        properties = request.env['estate.property'].search(domain, offset=(page-1) * properties_per_page, limit=properties_per_page)
        return request.render('estate.property_list_template',{
            'properties': properties,
            'pager': request.website.pager(
                url="/properties",
                total=total_properties,
                page=page,
                step=properties_per_page,
                url_args={'listed_after': listed_after} if listed_after else {} 
            ),
            'listed_after': listed_after
        })

    @http.route('/property/<int:property_id>', type='http', auth="public", website=True)
    def property_info(self, property_id, **kwargs):
        Property = request.env['estate.property'].browse(property_id)
        if not Property.exists():
            return request.not_found()
        return request.render('estate.property_info_template',{
            'property': Property,
        })
