from odoo import api, fields, models
from datetime import timedelta


class PropertyOffers(models.Model):
    _name = "property.offers"
    _description = "Property Offers"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )

    # relationships
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    # inverse function fields
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            # need a fallback to prevent crashing at time of creation.
            create_date = record.create_date or fields.Datetime.now()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days
            else:
                record.validity = 7
