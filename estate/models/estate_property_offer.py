from datetime import timedelta

from odoo import api, fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float()

    validity = fields.Integer(
        default=7,
    )

    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )

    partner_id = fields.Many2one(
        "res.partner",
        required=True,
    )

    property_id = fields.Many2one(
        "estate.property",
        required=True,
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            create_date = (
                offer.create_date.date()
                if offer.create_date
                else fields.Date.today()
            )

            offer.date_deadline = (
                create_date +
                timedelta(days=offer.validity)
            )

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = (
                offer.create_date.date()
                if offer.create_date
                else fields.Date.today()
            )

            if offer.date_deadline:
                offer.validity = (
                    offer.date_deadline - 
                    create_date
                ).days
