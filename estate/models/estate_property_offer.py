from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
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
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    _sql_constraints = [
        (
            "check_price_positive",
            "CHECK(price >= 0)",
            "The price must be positive!",
        ),
        (
            "check_validity_positive",
            "CHECK(validity > 0)",
            "The validity must be positive!",
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_obj = self.env["estate.property"].browse(vals["property_id"])

            if vals.get("price", 0) < property_obj.best_price:
                raise UserError(
                    f"Cannot create an offer with price {vals.get('price', 0):,.2f}. "
                    f"An offer with a higher price ({property_obj.best_price:,.2f}) already exists."
                )

            if property_obj.state == "new":
                property_obj.state = "offer_received"

        return super().create(vals_list)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = (
                record.create_date and record.create_date.date()
            ) or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = (
                record.create_date and record.create_date.date()
            ) or fields.Date.today()
            if record.date_deadline:
                record.validity = (record.date_deadline - create_date).days

    def action_accept(self):
        for offer in self:
            if any(o.status == "accepted" for o in offer.property_id.offer_ids):
                raise UserError(
                    "Another offer has already been accepted for this property!"
                )

            offer.status = "accepted"
            offer.property_id.state = "offer_accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id

            # Cancel all other offers for this property
            other_offers = offer.property_id.offer_ids.filtered(
                lambda o: o.id != offer.id
            )
            other_offers.status = "refused"

        return True

    def action_refuse(self):  # Changed from action_reject
        for offer in self:
            offer.status = "refused"

            if not any(o.status == "accepted" for o in offer.property_id.offer_ids):
                offer.property_id.state = "offer_received"
                offer.property_id.buyer_id = False
                offer.property_id.selling_price = 0.0

        return True
