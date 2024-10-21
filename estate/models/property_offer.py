from dateutil.relativedelta import relativedelta

from odoo import models, fields, api


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The Offer Price must be positive.'),
        ('check_validity', 'CHECK(validity >= 0)', 'The Offer Validity must be positive.'),
    ]
    _order = 'price desc'

    state = fields.Selection([
        ('received', 'Received'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], default='received', required=True, readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    price = fields.Float()
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    create_date = fields.Date(string='Create Date', default=lambda self: fields.Datetime.now())
    validity = fields.Integer(string='Validity (days)', default=7)
    deadline_date = fields.Date(string='Deadline Date', compute='_compute_deadline_date',
                                inverse='_inverse_deadline_date')
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id')

    @api.depends('validity', 'deadline_date', 'create_date')
    def _compute_deadline_date(self):
        for record in self:
            record.deadline_date = record.create_date + relativedelta(days=record.validity)

    @api.depends('validity', 'deadline_date', 'create_date')
    def _inverse_deadline_date(self):
        for record in self:
            record.validity = (record.deadline_date - record.create_date).days

    def action_accept(self, propagate=True):
        for record in self:
            if propagate:
                record.property_id.set_accepted_offer(record)
            record.state = 'accepted'
        return True

    def action_refuse(self, propagate=True):
        for record in self:
            if record.state == 'accepted' and propagate:
                record.property_id.set_accepted_offer(None)
            record.state = 'refused'
        return True

    def action_reset(self, propagate=True):
        for record in self:
            if record.state == 'accepted' and propagate:
                record.property_id.set_accepted_offer(None)
            record.state = 'received'
        return True
