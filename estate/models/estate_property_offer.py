from datetime import timedelta
from odoo import api, fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer model'

    price = fields.Float(string='Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(compute='_compute_total_days', inverse='_inverse_total_days', string='Deadline')

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0.0)', 'The offer price must be strictly positive.')
    ]

    @api.depends('create_date', 'validity')
    def _compute_total_days(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_total_days(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            days = (record.date_deadline - create_date).days
            record.validity = days if days >= 0 else 0

    def action_accepted(self):
        self.status = 'accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price

    def action_refused(self):
        self.status = 'refused'
