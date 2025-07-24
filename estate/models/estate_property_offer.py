from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    _sql_constraints = [
        ("check_price_positive", "CHECK(price >= 0)", "The price must be positive!"),
        (
            "check_validity_positive",
            "CHECK(validity > 0)",
            "The validity must be positive!",
        ),
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(
                    days=record.validity
                )
            else:
                # Fallback for when create_date is not set yet
                record.date_deadline = fields.Date.today() + timedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days
            elif record.date_deadline:
                # Fallback for when create_date is not set yet
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for offer in self:
            # Check if another offer is already accepted for this property
            existing_accepted = self.search(
                [
                    ("property_id", "=", offer.property_id.id),
                    ("status", "=", "accepted"),
                    ("id", "!=", offer.id),
                ]
            )
            if existing_accepted:
                raise UserError(
                    "Another offer has already been accepted for this property!"
                )

            offer.status = "accepted"
            offer.property_id.state = "offer_accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id

            # Cancel all other offers for this property
            other_offers = self.search(
                [
                    ("property_id", "=", offer.property_id.id),
                    ("id", "!=", offer.id),
                    ("status", "!=", "refused"),
                ]
            )
            other_offers.write({"status": "refused"})

        return True

    def action_refuse(self):  # Changed from action_reject
        for offer in self:
            offer.status = "refused"

            # Only reset property state if no accepted offers remain
            remaining_accepted = self.search(
                [
                    ("property_id", "=", offer.property_id.id),
                    ("status", "=", "accepted"),
                ]
            )

            if not remaining_accepted:
                offer.property_id.state = "offer_received"
                offer.property_id.buyer_id = False
                offer.property_id.selling_price = 0.0

        return True
