from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    sell_type = fields.Selection(related='property_id.sell_type', store=True)

    @api.model_create_multi
    def create(self, vals):
        if isinstance(vals, list) and vals:
          vals = vals[0]
        property_id = vals.get('property_id')
        if not property_id:
            raise ValueError("Missing 'property_id' in values")
        property = self.env['estate.property'].browse(property_id)
        if vals['price'] < property.expected_price:
            raise exceptions.UserError(f"offer price must not be lower than expected price :  {property.expected_price}")
        return super(EstatePropertyOffer, self).create(vals)

    def action_accept(self):
        res = super(EstatePropertyOffer, self).action_accept()
        for offer in self:
            if offer.property_id.sell_type == 'auction' and offer.property_id.stage in ['template', 'sold']:
                raise exceptions.UserError("Property cannot be sold or accepted during the auction process.")

            offer.property_id.update({
                'stage': 'template'
            })
            # Notify the accepted bidder
            offer.partner_id.message_post(
                body=f"Congratulations! Your offer of {offer.price} has been accepted for {offer.property_id.name}.",
                subject="Your Offer Has Been Accepted!",
                message_type="comment",
                subtype_xmlid="mail.mt_comment"
            )
            other_offers = self.search([
                ('property_id', '=', offer.property_id.id),
                ('id', '!=', offer.id)
            ])
            #Notify rejected bidders
            for rejected_offer in other_offers:
                rejected_offer.partner_id.message_post(
                    body=f"Unfortunately, your offer of {rejected_offer.price} for {rejected_offer.property_id.name} was not accepted.",
                    subject="Your Offer Was Not Accepted",
                    message_type="comment",
                    subtype_xmlid="mail.mt_comment"
                )
        return res
