# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError


class EstateWebsiteController(http.Controller):

    @http.route(['/estate/property/<int:property_id>/offer'], type='http', auth="user", website=True)
    def property_offer_form(self, property_id, **kw):
        property_obj = request.env['estate.property'].sudo().browse(property_id)
        if not property_obj.exists() or not property_obj.auction_started or property_obj.auction_status != 'auction':
            return request.redirect('/properties')
        return request.render("estate_auction.property_offer_form", {
            'property': property_obj,
            'partner': request.env.user.partner_id
        })

    @http.route(['/estate/property/<int:property_id>/offer/submit'], type='http', auth="user", website=True, methods=['POST'])
    def property_offer_submit(self, property_id, **post):
        property_obj = request.env['estate.property'].sudo().browse(property_id)
        if not property_obj.exists() or not property_obj.auction_started or property_obj.auction_status != 'auction':
            return request.redirect('/properties')
        try:
            amount = float(post.get('amount', 0))
            partner_id = int(post.get('partner_id', 0))
            request.env['estate.property.offer'].sudo().create({
                'price': amount,
                'partner_id': partner_id,
                'property_id': property_id
            })
            return request.render("estate_auction.property_offer_confirmation", {'property': property_obj})
        except ValidationError as e:
            values = {
                'property': property_obj,
                'partner': request.env.user.partner_id,
                'error': str(e)
            }
            return request.render("estate_auction.property_offer_form", values)
