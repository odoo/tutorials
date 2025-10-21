from odoo import api, models, fields
import datetime


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "test description"

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_deadline', inverse='inverse_deadline')

    @api.depends('validity')
    def _compute_deadline(self):
        for records in self:
            records.date_deadline = fields.Datetime.add(fields.Date.today(), days=records.validity) 

    def inverse_deadline(self):
        for records in self:
            records.validity = (records.date_deadline - fields.Date.today()).days
