from odoo import api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    sale_type = fields.Selection(related="property_id.property_sale_type")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])

            if property.property_sale_type == 'auction':
                if vals['price'] < property.expected_price:
                    raise UserError(f"Offer must be at least {property.expected_price} INR. Your offer is {vals['price']} INR.")
                
                return super(models.Model, self).create(vals_list)
                
        return super().create(vals_list)

    def action_accept(self):
        self.ensure_one()

        if self.sale_type == 'auction' and self.property_id.auction_state in ['template', 'sold']:
            raise UserError("Offer cannot be accepted.")
        if self.property_id.state in ['sold', 'cancelled']:
            raise UserError("Sold/Cancelled property's offer can't be accepted!")
        if self.status == 'accepted':
            raise UserError("Offer is already accepted.")
            
        for offer in self.property_id.offer_ids:
            if offer.id == self.id:
                offer.status = "accepted"
                self.property_id.write(
                    {
                        'buyer_id': self.partner_id,
                        'selling_price': self.price,
                        'state': 'offer_accepted'
                    }
                )

                template = self.env.ref("estate_auction.mail_template_offer_accepted")
                template.send_mail(offer.id, force_send=True)

            else:
                offer.status = 'refused'

                template = self.env.ref("estate_auction.mail_template_offer_refused")
                template.send_mail(offer.id, force_send=True)
