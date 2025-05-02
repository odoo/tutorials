from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    is_parent_auction = fields.Boolean(
        string='Is Auction Offer', readonly=True, compute='_compute_is_parent_auction'
    )

    @api.depends('property_id.sale_mode')
    def _compute_is_parent_auction(self):
        for record in self:
            record.is_parent_auction = record.property_id.sale_mode == 'auction'

    @api.model_create_multi
    def create(self, offers):
        if not offers:
            return super().create(offers)

        estate = self.env['estate.property'].browse(offers[0].get('property_id'))
        if not estate.exists():
            raise ValidationError('The specified property does not exist.')

        if estate.sale_mode == 'regular':
            return super().create(offers)

        if estate.auction_state != '02_auction':
            raise ValidationError('The auction is not active.')

        if estate.state in ['sold', 'cancelled']:
            raise UserError(
                'You cannot create an offer on a sold or cancelled property.'
            )
        if estate.state == 'offer_accepted':
            raise UserError(
                'You cannot create an offer on a property with an accepted offer.'
            )

        for offer in offers:
            if offer['price'] < estate.expected_price:
                raise UserError(
                    'The offer price must be higher than the expected price.'
                )

        estate.state = 'offer_received'
        return models.Model.create(self, offers)

    def action_accept(self):
        super().action_accept()

        accept_mail = self.env.ref('estate_auction.offer_accepted_email')
        refuse_mail = self.env.ref('estate_auction.offer_refused_email')

        offers = self.property_id.offer_ids
        for record in self:
            offers_to_refuse = offers - record

            if accept_mail:
                accept_mail.sudo().send_mail(record.id, force_send=True)
            if refuse_mail:
                for offer in offers_to_refuse:
                    refuse_mail.sudo().send_mail(offer.id, force_send=True)

        return True
