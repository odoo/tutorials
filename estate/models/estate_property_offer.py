from dateutil import relativedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate: Offer"

    price = fields.Float("Price")
    status = fields.Selection(
        selection=[
            ("available", "Available"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_compute_deadline")

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends("validity")
    def _compute_deadline(self) -> None:
        for record in self:
            creation_date = record.create_date or fields.Date.today()
            record.date_deadline = creation_date + relativedelta.relativedelta(days=record.validity)

    def _inverse_compute_deadline(self) -> None:
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
