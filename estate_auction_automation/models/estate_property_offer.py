from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    # related field
    property_sell_type = fields.Selection(related='property_id.property_sell_type', store=True)

    def create(self, vals_list):
        """Bypasses all parent validations while creating offers"""
        return models.Model.create(self, vals_list)

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
