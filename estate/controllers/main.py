# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager


class EstateWebsite(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth="public", website=True)
    def properties_list(self, page=1, filter_date=None, search_name=None, **kwargs):
        Property = request.env['estate.property']
        domain = [('state', 'in', ['new', 'offer_received', 'offer_accepted'])]

        if search_name:
            domain.append(('name', '=', search_name))

        if filter_date:
            domain.append(('create_date', '>', filter_date))

        per_page = 6
        offset = (page - 1) * per_page
        properties = Property.search(domain, limit=per_page, offset=offset)
        count = Property.search_count(domain)
        pager = portal_pager(
            url='/properties',
            total=count,
            page=page,
            step=per_page,
            url_args={'filter_date': filter_date} if filter_date else {}
        )
        return request.render('estate.property_list_template',{
            'properties': properties,
            'pager': pager,
            'filter_date': filter_date,
            'search_name' : search_name
        })

    @http.route('/property/<int:property_id>', type='http', auth="public", website=True)
    def property_info(self, property_id, **kwargs):
        Property = request.env['estate.property'].browse(property_id)
        if not Property.exists():
            return request.not_found()
        
        return request.render('estate.property_info_template',{
            'property': Property,
        })
