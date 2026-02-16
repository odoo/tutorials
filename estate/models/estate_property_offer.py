from datetime import timedelta
from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ]
    )

    partner_id = fields.Many2one("res.partner", string="Partner")

    property_id = fields.Many2one("estate.property", string="Property")

    validity = fields.Integer(default=7, string="Validity (days)")

    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date
            if not base_date:
                base_date = fields.Date.today()
            else:
                base_date = base_date.date()

            record.date_deadline = base_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days
