from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    # related field
    sale_method = fields.Selection(related='property_id.sale_method', store=True)

    def action_accept(self):
        self.ensure_one()

        # Validate if the property can be sold
        if self.sale_method == 'auction' and self.property_id.state in ['01_template', '03_offer_accepted']:
            raise UserError("Offer cannot be accepted.")

        if self.property_id.status == 'sold':
            raise UserError("Property already sold.")                                                           
        if self.property_id.status == 'cancelled':
            raise UserError("Property is cancelled. Offers cannot be accepted.")
        if self.status == 'accepted':
            raise UserError("Buyer is already accepted.")

        # Fetch the unified email template
        template = self.env.ref('estate_auction_automation.estate_offer_notification_email')
                                                                                                                         
        accepted_buyer_id = self.partner_id.id
        rejected_buyers = set()

        # Process all offers
        for offer in self.property_id.offer_ids:
            is_accepted = offer.id == self.id

            offer.write({'status': 'accepted' if is_accepted else 'refused'})

            if is_accepted:
                self.property_id.write({
                    'selling_price': self.price,
                    'buyer_id': self.partner_id.id,
                    'status': 'offer_accepted'
                })

            # Send email notification
            if template and offer.partner_id.id not in rejected_buyers:
                template.with_context(
                    user_email=self.env.user.email,
                    partner_id=offer.partner_id.email,
                    partner_name=offer.partner_id.name,
                    property_name=self.property_id.name,
                    offer_amount=offer.price,
                    is_accepted=is_accepted,
                    user_signature=self.env.user.name,
                ).send_mail(offer.id, force_send=True)

                if not is_accepted:
                    rejected_buyers.add(offer.partner_id.id)
