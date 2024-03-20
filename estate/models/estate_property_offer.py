from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'An offer for a property'

    price = fields.Float(default=0.0)
    status = fields.Selection([
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], default='new', copy=False)

    partner_id = fields.Many2one('res.partner', string='Buyer')
    property_id = fields.Many2one('estate.property', string='Property')

    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_deadline', inverse='_inverse_deadline')

    create_date = fields.Date('Date Created')

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = \
                record.create_date + relativedelta(days=record.validity) \
                    if record.create_date and record.validity != None else None

    def _inverse_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                print(f'diff: {(record.date_deadline - record.create_date).days}')
                record.validity = (record.date_deadline - record.create_date).days
