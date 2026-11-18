from odoo import api, fields, models
from odoo.tools import date_utils


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer"

    price = fields.Float('Price', copy=False)
    validity = fields.Integer('Validity Period of the Offer', default=7)
    date_deadline = fields.Date('Deadline for this offer', compute="_compute_deadline", inverse="_inverse_deadline")
    state = fields.Selection(
        string='Status',
        selection=[('draft', 'Draft'), ('accepted', 'Accepted'), ('refused', 'Refused')],
        default='draft',
        required=True
    )
    buyer_id = fields.Many2one('res.partner', string='Buyer', required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    @api.depends("create_date")
    def _util_from_date(self, record):
        return record.create_date.date() if record.create_date else fields.Date.today()

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = date_utils.add(self._util_from_date(record), days=+record.validity)

    @api.depends("validity")
    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - self._util_from_date(record)).days

    def action_accept(self):
        for record in self:
            record.state = 'accepted'

    def action_refuse(self):
        for record in self:
            record.state = 'refused'
