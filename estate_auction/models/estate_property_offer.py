from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    is_auction = fields.Boolean(
        string="Auction Offer", related="property_id.is_auction", readonly=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])

            if (
                property_id.property_selling_type != 'auction'
                or property_id.auction_stages != 'active'
            ):
                return super().create(vals_list)

                continue
            if property_id.state == 'sold':
                raise UserError("You can't create offer on sold properties")
            if property_id.state != 'offer_received':
                property_id.state = 'offer_received'
            if vals['price'] < property_id.expected_price:
                raise ValidationError(
                    "The offer price must be greater than or equal to the expected price."
                )
            return models.Model.create(self, vals_list)

    def action_estate_property_offer_accept(self):
        super().action_estate_property_offer_accept()

        template_accept = self.env.ref('estate_auction.email_template_offer_accepted')
        template_refuse = self.env.ref('estate_auction.email_template_offer_refused')

        offers = self.property_id.offer_ids
        for record in self:

            offers_to_refuse = offers - record

            if template_accept:
                template_accept.sudo().send_mail(record.id, force_send=True)

            if template_refuse:
                for offer in offers_to_refuse:
                    template_refuse.sudo().send_mail(offer.id, force_send=True)
