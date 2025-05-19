from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    """Model representing an offer made on a real estate property.

    This model manages offers submitted by buyers for properties, including offer price,
    validity period, and status (accepted or refused). It ensures offers are valid, updates
    property states, and validations such as unique accepted offers and minimum
    offer prices.
    """

    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "offer_price desc"

    offer_price = fields.Float(string="Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one(
        "estate.property", string="Property", required=True, ondelete="cascade"
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Date Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _sql_constraints = [
        (
            "check_offer_price_positive",
            "CHECK(offer_price > 0)",
            "The offer price must be strictly positive.",
        ),
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        """Compute the offer's deadline based on its validity period.

        Calculates the `date_deadline` by adding the `validity` (in days) to the offer's
        creation date. If no creation date exists, uses the current date.
        """
        for record in self:
            create_date = record.create_date or fields.Date.context_today(record)
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        """Update the validity period based on the deadline date.

        Computes the `validity` (in days) as the difference between the `date_deadline`
        and the offer's creation date. If no creation date exists, uses the current date.
        """
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            delta = record.date_deadline - create_date.date()
            record.validity = delta.days

    def action_accept(self):
        """Accept the offer and update the associated property.

        Marks the offer as 'accepted', sets the property's buyer, selling price, and state
        to 'offer_accepted'. Ensures no other offers are already accepted and the property
        is not sold or canceled.
        """
        for record in self:
            if record.property_id.state in ["sold", "canceled"]:
                raise UserError(
                    "You cannot accept an offer for a sold or cancelled property."
                )
            if record.property_id.state == "offer_accepted":
                raise UserError("An offer has already been accepted for this property.")

            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.offer_price
            record.property_id.state = "offer_accepted"

    def action_refuse(self):
        """Refuse the offer.

        Updates the offer's status to 'refused'.
        """
        for record in self:
            record.status = "refused"

    @api.model_create_multi
    def create(self, offers):
        """Create one or more offers with validation checks.

        Ensures the property exists, is not sold or canceled, and does not have an accepted
        offer. Validates that each offer's price is higher than the current best offer price.
        Updates the property's state to 'offer_received' upon successful creation.
        """
        if not offers:
            raise ValidationError("No offers provided for creation.")

        property_id = offers[0].get("property_id")
        if not property_id:
            raise ValidationError("Property ID is required.")

        estate = self.env["estate.property"].browse(property_id)
        if not estate.exists():
            raise ValidationError("The specified property does not exist.")

        if estate.state in ["sold", "canceled"]:
            raise UserError("Cannot create an offer on a sold or canceled property.")
        if estate.state == "offer_accepted":
            raise UserError(
                "Cannot create an offer on a property with an accepted offer."
            )

        curr_max_price = estate.best_price or 0.0

        for offer in offers:
            if curr_max_price >= offer["offer_price"]:
                raise UserError(
                    "The offer price must be higher than the current best price."
                )
            curr_max_price = max(curr_max_price, offer["offer_price"])

        estate.state = "offer_received"
        return super().create(offers)
