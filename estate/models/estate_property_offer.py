from datetime import timedelta, datetime

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models


class EstatePpropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate property offer description'
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'A offer price must be strictly positive.')
    ]
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False,
    )

    # offer Many2one relation with res.partner
    partner_id = fields.Many2one(
        'res.partner',
        required=True
    )

    # offer Many2one realtion with property
    property_id = fields.Many2one(
        'estate.property',
        required=True
    )

    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadDeadline", inverse="_inverse_deadDeadline", store=True)

    @api.depends("validity")
    def _compute_deadDeadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = datetime.now() + timedelta(days=record.validity)

    def _inverse_deadDeadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_offer_accepted(self):
        for record in self:
            if record.property_id.buyer_id:
                raise UserError("This Property has already accepted an offer.")
            else:
                record.status = 'accepted'
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
        return True

    def action_offer_refused(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.buyer_id = False
                record.property_id.selling_price = False
            self.status = 'refused'
        return True

    @api.model
    def create(self, vals_list):
        property_id = self.env['estate.property'].browse(vals_list['property_id'])
        if vals_list['price'] < property_id.best_offer_price:
            raise ValidationError("You can not create offer with a lower amount than an existing offer.")
        property_id.state =  'offer_received'
        return super(EstatePpropertyOffer, self).create(vals_list)
