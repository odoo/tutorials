from odoo import models, fields, api
from datetime import timedelta


class EstateOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer Model"

    price = fields.Float()
    status = fields.Selection(
        [("Accepted", "Accepted"), ("Refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(default=fields.Date.today() + timedelta(days=7))

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                (record.create_date or fields.date.today()), days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (
                (record.date_deadline - record.create_date.date()).days
                if record.date_deadline
                else 0
            )
