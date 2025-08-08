from datetime import datetime

from odoo import _ , fields , http
from odoo.http import request


class EstateAuctionWebsite(http.Controller):
    @http.route(['/property/<model("estate.property"):property>/offer'], type='http', auth='user', website=True)
    def property_make_offer(self, property, **kwargs):
        """Display the form to make an offer on a property"""
        partner = request.env.user.partner_id
        return request.render('estate_auction.property_make_offer_page', {
            'property': property,
            'partner': partner,
        })

    @http.route(['/property/<model("estate.property"):property>/offer/submit'], type='http', auth='user', website=True, methods=['POST'])
    def property_submit_offer(self, property, **post):
        """Handle the submission of an offer"""
        amount = float(post.get('amount', 0))
        partner_id = request.env.user.partner_id.id

        if amount <= 0:
            return request.render('estate_auction.property_offer_error', {
                'property': property,
                'error_message': _("Offer amount must be greater than zero.")
            })

        # Check if the amount is higher than the expected price
        if amount < property.expected_price:
            return request.render('estate_auction.property_offer_error', {
                'property': property,
                'error_message': _("Your offer must be at least the expected price (%.2f).", property.expected_price)
            })

        # Create the offer
        offer_vals = {
            'property_id': property.id,
            'partner_id': partner_id,
            'price': amount,
        }

        request.env['estate.property.offer'].sudo().create(offer_vals)
        
        return request.render('estate_auction.property_offer_success', {
            'property': property,
        })
