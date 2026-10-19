from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
        string="Status",
    )
    partner_id = fields.Many2one("res.partner", string="partner", required=True)
    property_id = fields.Many2one("estate.property", string="property", required=True)

    validity = fields.Integer(default=7, string="validity (days)")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = (
                offer.create_date.date() if offer.create_date else fields.date.today()
            )
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - date).days
