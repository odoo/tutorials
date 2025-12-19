from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "A property offer"

    price = fields.Float('Price')
    status = fields.Selection(selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
        ], copy=False, string='Status')
    property_buyer_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer('Validity (Days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_date_deadline', inverse='_inverse_validity')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            starting_date = record.create_date if record.create_date else fields.Date.context_today(self)
            record.date_deadline = starting_date + relativedelta(days=record.validity)

    def _inverse_validity(self):
        for record in self:
            starting_date = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.context_today(self)
            record.validity = (record.date_deadline - starting_date).days
