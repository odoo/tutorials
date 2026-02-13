from datetime import timedelta
from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(required=True, string="Offer Price")
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True, string="Property")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ("accepted", "Accepted"),
            ("refuse", "Refused"),
        ],
    )
    validity = fields.Integer(
        string="Validity",
        default=7,
        compute="_compute_validity",
        inverse="_inverse_validity",
    )
    date_deadline = fields.Date(
        string="Deadline Date",
        default=lambda self: fields.Date.today() + timedelta(days=7),
    )

    @api.depends("date_deadline")
    def _compute_validity(self):
        for record in self:
            if record.date_deadline:
                today = fields.Date.today()
                record.validity = (record.date_deadline - today).days

    def _inverse_validity(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(days=record.validity)
