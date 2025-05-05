# models/estate_property_offer.py
from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        default="refused",
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True
    )

    property_type_id = fields.Many2one(
        related="property_id.property_type_id", string="Property Type", store=True
    )

    # SQL Constrains
    _sql_constraints = [
        (
            "check_offer_price_positive",
            "CHECK(price >= 0)",
            "The offer price must be strictly positive.",
        ),
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            # Fallback to today if create_date is not set
            base_date = offer.create_date or fields.Datetime.now()
            offer.date_deadline = base_date.date() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            base_date = offer.create_date or fields.Datetime.now()
            if offer.date_deadline:
                delta = offer.date_deadline - base_date.date()
                offer.validity = delta.days

    # Buttons
    status = fields.Selection(
        [("new", "New"), ("accepted", "Accepted"), ("refused", "Refused")],
        required=True,
        copy=False,
        default="new",
    )

    def action_accept(self):
        for offer in self:
            if offer.status != "new":
                raise UserError("An offer has already been processed.")
            offer.status = "accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = "offer_accepted"

    def action_refuse(self):
        for offer in self:
            if offer.status != "new":
                raise UserError("An offer has already been processed.")
            offer.status = "refused"

    # CRUD Functions
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")
            if property_id:
                property = self.env["estate.property"].browse(property_id)

                # Check for higher existing offer
                existing_max = self.env["estate.property.offer"].search(
                    [("property_id", "=", property_id)], limit=1, order="price DESC"
                )

                if existing_max and vals.get("price", 0.0) < existing_max.price:
                    raise ValidationError("Offer must be higher than existing offers.")

                # Set state to 'offer_received'
                if property.state == "new":
                    property.state = "offer_received"

        return super().create(vals_list)
