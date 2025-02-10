from odoo import api, fields, models
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"
    price = fields.Float("Price")
    state = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy=False,
        default="accepted",
    )
    partner_id = fields.Many2one("res.partner", string="Partner Id", required=True)
    property_id = fields.Many2one(
        "estate.property", string="Property Id", required=True
    )
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date(
        "Date Deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(
                    days=record.validity
                )
            else:
                # fallback: if create_date is not set then set it to current date
                record.date_deadline = fields.Date.today() + timedelta(
                    days=record.validity
                )

    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline:
                if record.create_date:
                    record.validity = (
                        record.date_deadline - record.create_date.date()
                    ).days
                else:
                    record.validity = 7
