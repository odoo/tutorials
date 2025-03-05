from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    # related field
    property_sell_type = fields.Selection(related='property_id.property_sell_type', store=True)

    # -------------------------------------------------------------------------
    # CRUD OPERATIONS
    # -------------------------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        """Bypasses all parent validations while creating offers, ensuring constraints for auction-type properties."""
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])

            if property.property_sell_type == 'auction':
                # Ensure offer price is at least equal to the expected price
                expected_price = property.expected_price

                if vals['price'] < expected_price:
                    raise UserError(
                        f"The offer price ({vals['price']}) must be at least equal to the expected price ({expected_price}).")
                
                return super(models.Model, self).create(vals_list)
                
        return super().create(vals_list)

    # ------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------

    def action_accept(self):
        self.ensure_one()
        
        # Validate if the property can be sold
        if self.property_sell_type == 'auction' and self.property_id.state in ['01_template', '03_offer_accepted']:
            raise UserError("Offer cannot be accepted.")

        if self.property_id.stage == 'sold':
            raise UserError("Property already sold.")
        if self.property_id.stage == 'cancelled':
            raise UserError("Property is cancelled. Offers cannot be accepted.")
        if self.status == 'accepted':
            raise UserError("Buyer is already accepted.")

        # Fetch email templates
        template_accept = self.env.ref('estate_auction_automation.estate_offer_acceptance_email')
        template_reject = self.env.ref('estate_auction_automation.estate_offer_refusal_email')

        accepted_buyer_id = self.partner_id.id
        rejected_buyers = set()

        # Process all offers
        for offer in self.property_id.offer_ids:
            if offer.id == self.id:
                # Accept the current offer
                offer.write({'status': 'accepted'})
                self.property_id.write({
                    'selling_price': self.price,
                    'buyer_id': self.partner_id.id,
                    'stage': 'offer_accepted'
                })

                # Send acceptance email
                if template_accept:
                    template_accept.with_context(
                        user_email=self.env.user.email,
                        partner_id=self.partner_id.email,
                        partner_name=self.partner_id.name,
                        property_name=self.property_id.name,
                        offer_amount=self.price,
                        user_signature=self.env.user.name,
                    ).send_mail(offer.id, force_send=True)

            else:
                # Reject all other offers
                offer.write({'status': 'refused'})

                # Ensure a rejected buyer gets only one email
                if template_reject and offer.partner_id.id != (
                    accepted_buyer_id and 
                    offer.partner_id.id not in rejected_buyers
                ):
                    template_reject.with_context(
                        user_email=self.env.user.email,
                        partner_id=offer.partner_id.email,
                        partner_name=offer.partner_id.name,
                        property_name=self.property_id.name,
                        offer_amount=offer.price,
                        user_signature=self.env.user.name,
                    ).send_mail(offer.id, force_send=True)
                    rejected_buyers.add(offer.partner_id.id)
