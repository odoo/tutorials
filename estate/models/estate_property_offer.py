from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True, copy=False)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_date_deadline', inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity", 'date_deadline')
    def _compute_date_deadline(self):
        for record in self:
            current_date = fields.Date.today()
            record.date_deadline = current_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            current_date = fields.Date.today()
            record.validity = relativedelta(record.date_deadline, current_date).days
