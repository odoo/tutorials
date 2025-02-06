from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    # Offer Fields
    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.today()).days
            else:
                record.validity = 7
    