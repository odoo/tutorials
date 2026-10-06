from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
            ("sold", "Sold"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer")
    property_id = fields.Many2one("estate.property", string="Property")
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True,
        string="Property Type",
    )
    _check_price = models.Constraint(
        "CHECK(price >= 0)",
        "The offer price must be strictly positive.",
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )

            if record.date_deadline:
                record.validity = (record.date_deadline - create_date).days

    def action_refuse(self):
        for record in self:
            record.status = "refused"

    def action_accept(self):
        if any(offer.status == "accepted" for offer in self.property_id.offer_ids):
            raise UserError("Only one offer can be accepted.")

        # Accept this offer
        self.status = "accepted"

        # Reject all other offers
        other_offers = self.env["estate.property.offer"].search(
            [
                ("property_id", "=", self.property_id.id),
                ("id", "!=", self.id),
            ]
        )

        other_offers.write({"status": "refused"})

        # Update property
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = "offer_accepted"

    def write(self, vals):
        for record in self:
            if record.property_id.state == "sold" and "price" in vals:
                raise UserError(
                    "You cannot change the offer price after the property is sold."
                )
            if record.property_id.state == "sold" and "status" in vals:
                raise UserError(
                    "You cannot change the offer status after the property is sold."
                )

            # If this offer is changed to Accepted,
            # refuse other accepted offers
            if vals.get("status") == "accepted":
                other_offers = self.env["estate.property.offer"].search(
                    [
                        ("property_id", "=", record.property_id.id),
                        ("id", "!=", record.id),
                        ("status", "=", "accepted"),
                    ]
                )

                other_offers.write({"status": "refused"})

        return super().write(vals)

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env["estate.property"].browse(vals["property_id"])

            if property.offer_ids and vals["price"] <= property.best_price:
                raise UserError(
                    "The offer price must be higher than the current best offer."
                )

            property.state = "offer_received"

        return super().create(vals_list)
