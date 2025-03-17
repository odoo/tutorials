import logging

from odoo import http
from odoo.http import request


_logger = logging.getLogger(__name__)


class EstateAuctionOffer(http.Controller):

    @http.route('/submit-offer/<int:property_id>', type='http', auth='user', website=True, methods=['POST'])
    def submit_offer(self, property_id, **kwargs):
        _logger.info("🔸 Received Offer Submission for Property ID: %s", property_id)
        _logger.info("🔹 Request Data: %s", kwargs)

        if not request.env.user:
            _logger.warning("User not authenticated.")
            return request.redirect('/')

        offer_price = kwargs.get('offer_price')

        if not offer_price:
            _logger.warning("Offer price is missing!")
            return request.redirect('/')

        try:
            offer_price = float(offer_price)
        except ValueError:
            _logger.error("Invalid offer price format: %s", offer_price)
            return request.redirect('/')

        property = request.env['estate.property'].sudo().browse(property_id)
        if not property.exists():
            _logger.error("Property not found with ID %s", property_id)
            return request.redirect('/')

        offer = request.env['estate.property.offer'].sudo().create({
            'property_id': property_id,
            'partner_id': request.env.user.partner_id.id,
            'price': offer_price,
        })

        _logger.info("✅ Offer Successfully Created: ID %s", offer.id)

        return request.render(
            'estate_auction.estate_auction_offer_success',
            {'property': property, 'offer': offer}
        )
