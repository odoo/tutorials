from typing import Required
from odoo import fields, models, api


class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "this is property offer model"

    price = fields.Float("price")
    status = fields.Selection(
        [("Accepted", "Accepted"), ("Refused", "Refused")], copy=False
    )
    validity = fields.Integer("validity", default=7)
    date_deadline = fields.Date(
        "date_deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("home.plan", required=True)

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                record.create_date or fields.Date.today(), days=record.validity
            )

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
