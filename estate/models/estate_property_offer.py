from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer"

    price = fields.Float(required=True)
    partner_id = fields.Many2one("res.partner", required=True, string="Buyer")
    status = fields.Selection(selection=[("awaiting", "Awaiting"), ("refused", "Refused"), ("accepted", "Accepted")], required=True, default="awaiting", copy=False)

    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            origin = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = origin + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            origin = record.create_date if record.create_date else fields.Date.today()
            # If there's a way to do this that's less verbose and doesn't require me to correct the duration with a +1, I'd love if you could show me
            record.validity = (datetime.combine(record.date_deadline, datetime.min.time()) - origin).days + 1
