from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import datetime as dt
from odoo.tools import float_compare

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', string='Deadline')
        
    _check_positive_price = models.Constraint(
        'CHECK(price > 0)',
        'Offer price must be strictly positive.'
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = record.create_date + dt.timedelta(days=record.validity) 

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for record in self:
            other_accepted = record.property_id.offer_ids.filtered(lambda o: o.status == 'accepted' and o != record)
            if other_accepted:
                raise UserError('An offer has already been accepted for this property!')
            record.status = 'accepted'
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    @api.constrains('price', 'status')
    def _check_selling_price_not_too_low(self):
        for record in self:
            if record.status == 'accepted' and float_compare(record.price, record.property_id.expected_price * 0.9, 2) < 0:
                raise ValidationError('The selling price must be atleast 90% of the expected price.')
