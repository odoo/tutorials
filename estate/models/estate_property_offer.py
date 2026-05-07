import datetime
import logging

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.orm.utils import ValidationError


_logger = logging.getLogger(__name__)


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offers'
    _order = 'price desc'

    deadline = fields.Date()
    partner_id = fields.Many2one(comodel_name='res.partner', required=True)
    price = fields.Float()
    property_id = fields.Many2one(comodel_name='estate.properties', readonly=True, required=True)
    property_type = fields.Char(related='property_id.property_type_id.type')
    property_type_id = fields.Many2one(related='property_id.property_type_id')
    status = fields.Selection(
        [
            ('refused', "Refused"),
            ('accepted', "Accepted")
        ],
        copy=False
    )
    validity = fields.Integer(compute="_compute_validity", inverse="_inverse_deadline", default=7)

    _check_offer_price = models.Constraint(
        'CHECK (price > 0)',
        "Offer price should be positive"
    )

    @api.depends('deadline')
    def _compute_validity(self):
        for offer in self:
            offer.validity = (offer.deadline - offer.create_date.date()).days if offer.deadline and offer.create_date else 7

    @api.depends('validity')
    def _inverse_deadline(self):
        for offer in self:
            # _logger.error(fields.Date.context_today(offer) + datetime.timedelta(days=offer.validity))
            # _logger.error(offer._fields)
            start_date = offer.create_date.date() if offer.create_date else fields.Date.context_today(offer)
            offer.deadline = start_date + datetime.timedelta(days=offer.validity)

    @api.model
    def create(self, val_list):
        # breakpoint()
        for val in val_list:
            current_price = val.get('price', 0)
            properties = self.env['estate.properties'].browse(val.get('property_id'))
            highest_offer = max(properties.mapped('offer_ids.price')) if properties.offer_ids else 0
            if val.get('price') < highest_offer:
                raise UserError(f"Offer price Rs.{current_price} is less than {highest_offer}!")
            # _logger.error(f"properties = {properties}")
            # _logger.error(f"current price = {current_price}")
        return super().create(val_list)

    # def unlink(self):
    #     for offer in self:
    #         if offer.status == 'accepted':
    #             raise UserError("Cannot delete an already accepted offer")
    #     return super().unlink()

    # @api.constrains('price')
    # def _check_price(self):
    #     for property in self:
    #         if property.price < 0:
    #             raise ValidationError("Value cannot be less than zero.")

    # @api.constrains('deadline')
    # def _check_deadline(self):
    #     for property in self:
    #         if property.deadline < fields.Date.context_today(property):
    #             raise ValidationError("Past dates not allowed")

    def _refuse_remaining_offers(self, offer_id, all_offers):
        # _logger.error(all_offers)
        for offer in all_offers:
            if offer.id != offer_id:
                offer.status = 'refused'

    def offer_accepted(self):
        # offer_id = 0
        # breakpoint()
        # for offer in self:
        #     if offer.status == 'accepted' and offer.property_id.state == 'offer_accepted':
        #         raise UserError("Property already accepted!")
        #     offer.status = 'accepted'
        #     all_offers = offer.property_id.offer_ids
        #     # _logger.error(all_offers)
        #     offer_id = offer.id
        #     offer._refuse_remaining_offers(offer_id, all_offers)
        #     offer.property_id.buyer_id = offer.partner_id
        #     offer.property_id.selling_price = offer.price
        #     offer.property_id.state = 'offer_accepted'
        # return True
        self.ensure_one()
        property = self.property_id
        if property.state == 'offer_accepted' and self.status == 'accepted':
            raise ValidationError("Property already accepted!")
        remaining_offers = property.offer_ids - self
        remaining_offers.write({
            'status': 'refused'
        })
        self.status = 'accepted'
        property.write({
            'buyer_id': self.partner_id,
            'selling_price': self.price,
            'state': 'offer_accepted',
        })
        return True

    def offer_refused(self):
        for offer in self:
            if offer.status == 'refused':
                raise UserError("Property already refused!")
            offer.status = 'refused'
        return True
