from odoo import http
from odoo.http import request
from odoo.exceptions import UserError


class PropertyOfferController(http.Controller):

    @http.route('/property/<int:property_id>/offer', type='http', auth="user", website=True)
    def property_offer_form(self, property_id):
        property = request.env['estate.property'].sudo().browse(property_id)
        user_partner = request.env.user.partner_id

        if not property.exists():
            return request.render('website.404')

        if property.property_sale_type == "auction":
            existing_offer = request.env['estate.property.offer'].search([
                ('property_id', '=', property_id),
                ('partner_id', '=', user_partner.id)
            ], limit=1)

            if existing_offer:
                return request.render('estate_auction.offer_already_exists', { 'offer': existing_offer })

        return request.render('estate_auction.property_offer_form', { 'property': property })

    @http.route('/property/submit-offer', type='http', auth="user", methods=['POST'], website=True)
    def submit_offer(self, **post):
        property_id = int(post.get('property_id'))
        offer_amount = float(post.get('offer_amount'))
        partner_id = request.env.user.partner_id.id 

        property = request.env['estate.property'].browse(property_id)

        if not property.exists():
            return request.render('website.404')

        try:
            request.env['estate.property.offer'].sudo().create({
                'property_id': property_id,
                'partner_id': partner_id,
                'price': offer_amount,
            })

            return request.render('estate_auction.offer_success_page')

        except UserError as e:
            return request.render('estate_auction.property_offer_form', {
                'property': property,
                'error_message': str(e), 
            })
