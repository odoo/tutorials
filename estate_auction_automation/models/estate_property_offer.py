from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    # related field
    property_sell_type = fields.Selection(related='property_id.property_sell_type', store=True)

    # -------------------------------------------------------------------------
    # CRUD OPERATIONS
    # -------------------------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        """Extend offer creation to check that the offer must be higher than expected price"""
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])
            
            # Prevent offer creation if the property is already sold
            if property.stage == 'sold':
                raise UserError(_("The offer cannot be created for a sold property."))

            max_price = property.best_price
            expected_price = property.expected_price

            # Check if the offer is higher than the current best price
            if vals['price'] <= max_price:
                raise UserError(_("The offer must be higher than %s.") % max_price)

            # Ensure the offer is also higher than the expected price
            if vals['price'] <= expected_price:
                raise UserError(_("The offer must be higher than the expected price of %s.") % expected_price)

            # Change property stage if it's still new
            if property.stage == 'new':
                property.stage = 'offer_received'

        return super().create(vals_list)

    # ------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------

    def action_accept(self):
        self.ensure_one()
        if self.property_sell_type == 'auction':
            return super().action_accept()

        if self.property_id.stage == 'sold':
            raise UserError("Property already sold.")
        elif self.property_id.stage == 'cancelled':
            raise UserError("Property cancelled, offers cannot be accepted.")
        elif self.status == 'accepted':
            raise UserError("Buyer is already accepted.")

        # Send mail to accepted partner
        template_accept = self.env.ref('estate_auction_automation.email_template_offer_accepted')

        # Send mail to rejected partners
        template_reject = self.env.ref('estate_auction_automation.email_template_offer_rejected')

        for offer in self.property_id.offer_ids:
            if offer.id != self.id:
                offer.status = 'refused'
                if template_reject:
                    template_reject.send_mail(offer.id, force_send=True)
            else:
                self.write({'status': 'accepted'})
                self.property_id.write({
                    'selling_price': self.price,
                    'buyer_id': self.partner_id.id,
                    'stage': 'offer_accepted'
                })
                if template_accept:
                    template_accept.send_mail(self.id, force_send=True)
