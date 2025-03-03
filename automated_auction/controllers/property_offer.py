from odoo import _
from odoo.http import Controller, request, route
from odoo.exceptions import UserError


class EstatePropertyOfferContoller(Controller):
    # Route For Add Offer in Particular Property
    @route(['/properties/<int:property_id>/add_offer'], type='http', auth="user", website=True)
    def add_offer_form(self, property_id, **kwargs):
        property_details = request.env['estate.property'].sudo().browse(property_id)

        return request.render('automated_auction.property_add_offer_template', {
            'property_details': property_details,
        })

    @route(['/properties/<int:property_id>/submit_offer'], type='http', auth="user", website=True)
    def add_offer_submit_form(self, property_id, **post):
        property_details = request.env['estate.property'].sudo().browse(property_id)

        offer_amount = float(post.get('offer_amount'))
        if offer_amount <= property_details.expected_price:
            raise UserError(_("Price must be greater than expected price"))

        # Create the offer in the estate.property.offer model
        request.env['estate.property.offer'].sudo().create({
            'property_id': property_id,
            'partner_id': request.env.user.partner_id.id,
            'price': offer_amount
        })

        return request.render('automated_auction.property_offer_added')
