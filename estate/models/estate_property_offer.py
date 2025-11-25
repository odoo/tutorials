from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    # ----------------------------------------
    # Private attributes
    # ----------------------------------------
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    # ----------------------------------------
    # Field declarations
    # ----------------------------------------
    price = fields.Float("Price")
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )

    # ----------------------------------------
    # SQL constraints
    # ----------------------------------------
    _offer_price_positive = models.Constraint("CHECK(price > 0)")

    # ----------------------------------------
    # Compute and inverse methods
    # ----------------------------------------
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date.date() + timedelta(days=offer.validity)
            else:  # Fallback if create_date is not set
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline and offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            elif offer.date_deadline:  # Fallback if create_date is not set
                offer.validity = (offer.date_deadline - fields.Date.today()).days

    # ----------------------------------------
    # CRUD methods
    # ----------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        # Validate offer amounts before creation
        for vals in vals_list:
            if "property_id" in vals and "price" in vals:
                # Get the property record
                property_record = self.env["estate.property"].browse(vals["property_id"])
                # Check if there are existing offers with higher or equal prices
                existing_offers = property_record.offer_ids
                if existing_offers:
                    max_existing_price = max(existing_offers.mapped("price"))
                    if vals["price"] <= max_existing_price:
                        msg = f"The offer amount must be higher than the existing offer of {max_existing_price}."
                        raise UserError(msg)

        # Create the offers
        offers = super().create(vals_list)
        # Update property status to 'offer_received' for all related properties
        offers.mapped("property_id").write({"status": "offer_received"})
        return offers

    # ----------------------------------------
    # Action methods
    # ----------------------------------------
    def action_accept_offer(self):
        for offer in self:
            # Check if there's already an accepted offer
            other_offers = offer.property_id.offer_ids - offer
            if any(other_offers.filtered(lambda o: o.status == "accepted")):
                error_msg = "An offer has already been accepted for this property."
                raise UserError(error_msg)
            offer.status = "accepted"
            # Refuse other offers for the same property
            other_offers.write({"status": "refused"})
            # Update the property status
            offer.property_id.status = "offer_accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.partner_id = offer.partner_id
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"
        return True
