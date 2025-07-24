from odoo import models, fields, api
from datetime import date, timedelta


class PropertyType(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer received for a property from partner'

    price = fields.Float('Price')
    status = fields.Selection(string='Status', selection=[(
        'accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(
        string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date if hasattr(
                record, 'create_date') and record.create_date else date.now()) + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            deadline = (record.date_deadline - record.create_date.date()).days
            record.validity = 0 if deadline < 0 else deadline
