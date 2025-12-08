from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class TestModel(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Model Offer'
    _order = 'price desc'

    price = fields.Float(default=0.00)
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(compute='_compute_validity', inverse='_inverse_validity', string='Validity (days)')
    date_deadline = fields.Date(string='Deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', string='Property Type', store=True)

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be a strictly positive value.'),
    ]

    @api.depends('date_deadline')
    def _compute_validity(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.today()).days
            else:
                record.validity = 0

    def _inverse_validity(self):
        for record in self:
            record.date_deadline = fields.Date.today()
            if record.validity:
                record.date_deadline += timedelta(days=record.validity)

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state in ['new', 'offer_received'] and record.status != 'refused':
                record.property_id.selling_price = record.price
                record.status = 'accepted'
                record.property_id.state = 'offer_accepted'
            else:
                message = {
                    'sold': 'cannot accept an offer on a sold property',
                    'cancelled': 'cannot accept an offer on a cancelled property',
                    'offer_accepted': 'cannot accept another offer on an accepted property',
                }
                raise UserError(self.env._(message[record.property_id.state]))
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if val['price'] <= self.env['estate.property'].browse(val['property_id']).best_price:
                raise UserError(self.env._('The offer price must be greater than the best offer.'))

            if self.env['estate.property'].browse(val['property_id']).state == 'new':
                self.env['estate.property'].browse(val['property_id']).state = 'offer_received'
        return super().create(vals)
