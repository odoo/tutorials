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
            property_id = val.get("property_id")
            # set state to offer_received
            if property_id:
                property_record = self.env["estate.property"].browse(property_id)
                property_record.status = "offer_received"

            # check if offer is there or not
            existing_offer = self.env["estate.property.offer"].search(
                [("property_id", "=", property_id), ("price", ">", val.get("price"))]
            )

            if existing_offer:
                raise UserError(
                    "You cannot create an offer with a lower amount than an existing offer"
                )
        return super(EstatePropertyOffer, self).create(vals)

    def action_accepted(self):
        for offer in self:
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
