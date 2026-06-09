from datetime import timedelta

from odoo import api, models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "It is estate property offer"

    price = fields.Float()

    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        copy=False,
    )

    partner_id = fields.Many2one("res.partner", required=True)

    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(string="Days", default=7)

    date_deadline = fields.Date(
        string="Deadline Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                if record.create_date:
                    delta = record.date_deadline - record.create_date.date()

                record.validity = delta.days
            else:
                record.validity = 7

