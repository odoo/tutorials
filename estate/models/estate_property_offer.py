from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api


class EstateProperOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer."

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline', string='Deadline')


    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=+record.validity)
            else:
                record.date_deadline = date.today() + relativedelta(days=+record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
