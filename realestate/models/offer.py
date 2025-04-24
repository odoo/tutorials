from odoo import api, fields, models
from datetime import timedelta


class Offer(models.Model):
    _name = "offer"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")])
    buyer_id = fields.Many2one("buyer")
    property_id = fields.Many2one("realestate")
    validity = fields.Integer()
    deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.deadline = record.property_id.date_availability + timedelta(
                days=record.validity
            )

    def _inverse_deadline(self):
        for record in self:
            record.validity = (
                record.deadline - record.property_id.date_availability
            ).days
