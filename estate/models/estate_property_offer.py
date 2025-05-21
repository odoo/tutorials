from datetime import date, timedelta

from odoo import api, fields, models


class TestModel(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Model Offer'

    price = fields.Float(default=0.00)
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(compute='_compute_validity', inverse='_inverse_validity', string='Validity (days)')
    date_deadline = fields.Date(string='Deadline')

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
