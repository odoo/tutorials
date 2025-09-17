from datetime import date
from odoo import api, models, fields
from odoo.exceptions import UserError

from odoo.orm.domains import timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"

    _order = 'price desc'

    price = fields.Float("Price")
    status = fields.Selection(
        [('accepted', "Accepted"), ('refused', "Refused")], copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(
            'estate.property.type',
            related='property_id.property_type_id')

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline')

    _check_price_positive = models.Constraint(
            'CHECK(price > 0)',
            "The offer price must be a positive value")

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = date.today() + timedelta(record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - date.today()).days

    def action_accept(self):
        if len(self) > 1:
            raise UserError("Can't accept more than one offer")
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
            for refused in record.property_id.offer_ids:
                if refused != record:
                    refused.status = 'refused'

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
