# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.estate.controllers.property import PropertyController
from datetime import datetime

from odoo import http
from odoo.http import request


class PropertyControllerInherit(PropertyController): 
    @http.route(['/properties','/properties/page/<int:page>'], type='http', auth='public', website=True)
    def list_properties(self, page=1, listed_after=None, sale_type=None, search_name=None):
        domain = [('state', 'in', ['new', 'offer_received'])]

        if listed_after:
            try:
                date_filter = datetime.strptime(listed_after, '%Y-%m-%d')
                domain.append(('create_date', '>=', date_filter))
            except ValueError:
                pass
        if sale_type == 'regular':
            domain.append(('is_auction_started', '=', False))
        elif sale_type == 'auction':
            domain.append(('is_auction_started', '=', True))
        if search_name:
            domain.append(('name', '=', search_name))

        properties_per_page = 6
        total_properties = request.env['estate.property'].search_count(domain)
        properties = request.env['estate.property'].search(
            domain,
            order='create_date DESC',
            offset=(page - 1) * properties_per_page,
            limit=properties_per_page
        )

        pager = request.website.pager(
            url='/properties',
            total=total_properties,
            page=page,
            step=properties_per_page,
            url_args={'listed_after': listed_after, 'sale_type': sale_type} if listed_after or sale_type else {} 
        )

        return request.render('estate.property_list_template', {
            'properties': properties,
            'pager': pager,
            'listed_after': listed_after,
            'sale_type': sale_type,
        })

    @http.route('/property/<int:property_id>/offer', auth='public', website=True, methods=['GET','POST'])
    def property_offer(self, property_id, **post):
        """Handles both GET (show form) and POST (process form) requests."""
        property_rec = request.env['estate.property'].sudo().browse(property_id)
        if not property_rec.exists():
            return request.not_found()
        
        if request.httprequest.method == 'POST':
            offer_name = post.get('offer_name')
            offer_amount = post.get('offer_amount')

            if offer_amount:
                offer_amount = float(offer_amount)

            request.env['estate.property.offer'].sudo().create({
                'price': offer_amount,
                'partner_id': request.env.user.partner_id.id,
                'property_id': property_id,
            })
            return request.redirect('/property/%d/offer/success' % property_id)
        
        return request.render('estate_auction.offer_form_template', {
            'property': property_rec,
        })

    @http.route('/property/<int:property_id>/offer/success', auth='public', website=True)
    def property_added_offer(self, property_id):
        property_rec = request.env['estate.property'].sudo().browse(property_id)
        if not property_rec.exists():
            return request.not_found()
        return request.render('estate_auction.offer_add_success_template', {
            'property': property_rec,
        })
