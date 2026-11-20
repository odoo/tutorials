from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer"

    price = fields.Float('Price', digits=(12, 2), required=True)
    partner = fields.Many2one("res.partner", string='Partner', required=True)
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    property_id = fields.Many2one("estate.property", "property_id", required=True, readonly=True)

    validity_days = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity_days', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()

            record.date_deadline = start_date + relativedelta(days=record.validity_days)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            delta_dates = record.date_deadline - start_date
            record.validity_days = delta_dates.days
