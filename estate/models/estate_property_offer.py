from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class EstatePropertyType(models.Model):
    _name = 'estate.property.offer'
    _description = "An offer made on a property"

    price = fields.Float(string='Price')
    status = fields.Selection(copy=False, selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ])
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date + relativedelta(days=record.validity)) if record.create_date else (fields.Date.today() + relativedelta(days=record.validity))
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = relativedelta(record.date_deadline, record.create_date if record.create_date else fields.Date.today()).days
