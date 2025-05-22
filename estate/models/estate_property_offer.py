from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class EstatePropertyTag(models.Model):
    _name = "estate.property.offer"
    _description = "real esate properties offers"

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    property_id = fields.Many2one('estate.property', 'Property', required=True)

    validity = fields.Integer('Validity (Days)', default=7)
    date_deadline = fields.Date('Deadline',compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if not record.validity:
                record.date_deadline = False
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if not record.date_deadline:
                record.validity = 0
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days
