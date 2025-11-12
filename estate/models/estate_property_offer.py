from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"
    _order = "price desc"

    _sql_constraints = [
        (
            "price_positive",
            "CHECK(price > 0)",
            "The offer price must be strictly positive.",
        )
    ]

    price = fields.Float("Price", required=True)
    state = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        string="State",
        copy=False,
        default=False,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner Id", required=True
    )
    property_id = fields.Many2one(
        comodel_name="estate.property", string="Property Id", required=True
    )
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date(
        "Date Deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )

    property_type_id = fields.Many2one(
        comodel_name="property.type",
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(
                    days=record.validity
                )
            else:
                # fallback: if create_date is not set then set it to current date
                record.date_deadline = fields.Date.today() + timedelta(
                    days=record.validity
                )

    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline:
                if record.create_date:
                    record.validity = (
                        record.date_deadline - record.create_date.date()
                    ).days
                else:
                    record.validity = 7

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property = self.env["estate.property"].browse(val["property_id"])
            max_offer_price = max(property.offer_ids.mapped("price") or [0])

            if property:
                if property.status == "sold":
                    raise UserError("You cannot create an offer for a sold property")
                elif val.get("price") < max_offer_price:
                    raise UserError(
                        "New offer should contain price higher than current one"
                    )

            property.status = "offer_received"
        return super().create(vals)

    def action_accepted(self):
        for offer in self:
            if offer.state == "accepted":
                raise UserError("This offer is already accepted")

            offer.state = "accepted"

            for other_offers in offer.property_id.offer_ids:
                if other_offers.id != offer.id:
                    other_offers.state = "refused"

            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.status = "offer_accepted"
        return True

    def action_refused(self):
        for offer in self:
            offer.state = "refused"
        return True
