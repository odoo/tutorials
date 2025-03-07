from datetime import date, timedelta
from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers on Estate Listed"

    price = fields.Float(string="Offered Price", required=True)
    validity = fields.Integer(string="Validity(in days)", default=7)
    deadline = fields.Date(
        compute="_compute_deadline",
        inverse="_inverse_validity",
        store=True,
        default=lambda self: date.today() + timedelta(days=7),
        copy=False,
    )
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        inverse="_inverse_validity",
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            create_date = (
                record.create_date.date() if record.create_date else date.today()
            )
            record.deadline = create_date + timedelta(days=record.validity)

    def _inverse_validity(self):
        for record in self:
            create_date = (
                record.create_date.date() if record.create_date else date.today()
            )
            if record.deadline:
                record.validity = (record.deadline - create_date).days
                