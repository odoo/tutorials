from datetime import timedelta
from odoo import api, fields, models


class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Show offer given by buyer"

    price = fields.Float()
    status = fields.Selection(
        selection=[("Accepted", "Accepted"), ("Refused", "Refused")],
        string="Status",
        copy=False,
    )

    partner_id = fields.Many2one("res.partner", required=True, string="Buyer")
    property_id = fields.Many2one(
        "estate.property", required=True
    )  # Many2one use for One2many

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline Date",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.validity = (
                (record.date_deadline - create_date).days if record.date_deadline else 0
            )
