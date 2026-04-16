import datetime
import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offers'

    deadline = fields.Date()
    partner_id = fields.Many2one(comodel_name='res.partner', required=True)
    price = fields.Float()
    property_id = fields.Many2one(comodel_name='estate.properties', readonly=True)
    status = fields.Selection(
        [
            ('refused', "Refused"),
            ('accepted', "Accepted")
        ],
        copy=False
    )
    validity = fields.Integer(compute="_compute_validity", inverse="_inverse_deadline")

    @api.depends('deadline')
    def _compute_validity(self):
        for offer in self:
            offer.validity = (offer.deadline - offer.create_date.date()).days if offer.deadline and offer.create_date else 0

    @api.depends('validity')
    def _inverse_deadline(self):
        for offer in self:
            # _logger.error(fields.Date.context_today(offer) + datetime.timedelta(days=offer.validity))
            # _logger.error(offer._fields)
            start_date = offer.create_date.date() if offer.create_date else fields.Date.context_today(offer)
            offer.deadline = start_date + datetime.timedelta(days=offer.validity)

    @api.constrains('price')
    def _check_price(self):
        for property in self:
            if property.price < 0:
                raise ValidationError("Value cannot be less than zero.")
    
    @api.constrains('deadline')
    def _check_deadline(self):
        for property in self:
            if property.deadline < fields.Date.context_today(property):
                raise ValidationError("Past dates not allowed")
