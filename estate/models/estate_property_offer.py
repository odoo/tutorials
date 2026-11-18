from datetime import timedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'),
                ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    def _get_create_date(self):
        return fields.Date.to_date(self.create_date) or fields.Date.today()

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record._get_create_date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record._get_create_date()).days
