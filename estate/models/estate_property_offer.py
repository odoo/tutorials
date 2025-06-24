from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"
    # SQL Constraints
    _sql_constraints = [
        (
            "check_offer_price_positive",
            "CHECK(price > 0)",
            "The offer price must be strictly positive.",
        )
    ]

    validity = fields.Integer(
        "Valid For", default=7, help="Number of days until this offer expires"
    )

    price = fields.Float(string="Offer Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False
    )
    # Relational Fields
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
        readonly=True,
    )
    # Computed fields
    date_deadline = fields.Datetime(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    @api.model
    def create(self, vals):
        # Fetch the property ID from the incoming data
        property_id = vals.get("property_id")
        new_offer_price = vals.get("price")

        # Safeguard in case required data is missing
        if not property_id or not new_offer_price:
            raise ValidationError(_("Both price and property must be provided."))

        # Get the actual property record
        property_rec = self.env["estate.property"].browse(property_id)

        # Compare offer price with existing offers
        existing_prices = property_rec.offer_ids.mapped("price")
        if existing_prices and new_offer_price < max(existing_prices):
            raise ValidationError(_("Offer must be higher than existing offers."))

        # Update property state if needed
        if property_rec.state == "new":
            property_rec.state = "offer_received"

        # Create the offer
        return super().create(vals)

    # Computed functions
    @api.depends("validity")
    def _compute_date_deadline(self):
        for estate_offer in self:
            create_date = estate_offer.create_date or fields.Date.today()
            estate_offer.date_deadline = create_date + timedelta(
                days=estate_offer.validity
            )

    def _inverse_date_deadline(self):
        for estate_offer in self:
            create_date = estate_offer.create_date or fields.Date.today()
            if estate_offer.date_deadline:
                delta = estate_offer.date_deadline - create_date
                estate_offer.validity = delta.days

    # Actions
    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.state == "sold":
                raise UserError(_("You cannot accept an offer on a sold property."))
            if offer.property_id.state == "offer_accepted":
                raise UserError(
                    _("An offer has already been accepted for this property.")
                )

            offer.status = "accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = "offer_accepted"

            # Refuse all other offers
            other_offers = offer.property_id.offer_ids - offer
            other_offers.write({"status": "refused"})
        return True

    def action_refuse_offer(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError(
                    _("You cannot refuse an offer that has already been accepted.")
                )
            offer.status = "refused"
        return True
