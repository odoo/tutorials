from odoo import api, fields, models
from datetime import datetime, timedelta

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Test description for estate.property.offer model"

    price         = fields.Float()
    status        = fields.Selection(
        string="Offer Status",
        copy=False,
        selection=[("accepted","Accepted"), ("refused", "Refused")])
    partner_id    = fields.Many2one("res.partner", required=True)
    property_id   = fields.Many2one("estate.property", required=True)
    validity      = fields.Integer(default=7, compute="_inverse_date_deadline", inverse="_computed_date_deadline")
    date_deadline = fields.Date(compute="_computed_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity")
    def _computed_date_deadline(self):
        for record in self:
            # record.create_date is "falsy" so if checking with `record.create_date if hasattr(record.create_date) else datetime.today()` then it's true because it hasattr but it's None so it's converted to false
            record.date_deadline = ((record.create_date or datetime.today()) + timedelta(days=record.validity)).date()

    @api.depends("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days