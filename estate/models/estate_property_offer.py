from datetime import timedelta

from odoo import api, exceptions, fields, models


class TestModel(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Model Offer'

    price = fields.Float(default=0.00)
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(compute='_compute_validity', inverse='_inverse_validity', string='Validity (days)')
    date_deadline = fields.Date(string='Deadline')

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
            if record.validity:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today()

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state in ['new', 'offer_received'] and record.status != 'refused':
                record.status = 'accepted'
                record.property_id.state = 'offer_accepted'
                record.property_id.selling_price = record.price
            else:
                message = {
                    'sold': 'cannot accept an offer on a sold property',
                    'cancelled': 'cannot accept an offer on a cancelled property',
                    'offer_accepted': 'cannot accept another offer on an accepted property',
                }
                raise exceptions.UserError(message=message[record.property_id.state])
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True
