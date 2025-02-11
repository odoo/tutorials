from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float("Price", required=True) # Offer details
    status = fields.Selection([
        ("draft", "Draft"),
        ("accepted", "Accepted"),
        ("refused", "Refused")
    ], string="Status", default="draft") # Status of the offer
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Property")
    property_type_id = fields.Many2one(related="property_id.property_type", store=True)

    validity = fields.Integer("Validity", default=7)

    _sql_constraints = [
        ("positive_offer_price", "CHECK(price > 0)",
         "A property offer price must be strictly positive.")
    ]

    date_deadline = fields.Date(
        string="Date Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    @api.depends("property_id.create_date", "validity")
    def _compute_date_deadline(self):
        """
        Compute the deadline date based on property creation date and validity period.
        """
        for record in self:
            if record.property_id and record.property_id.create_date:
                record.date_deadline = record.property_id.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = False  # Prevents crashes if create_date is missing

    def _inverse_date_deadline(self):
        """
        Allow the user to set either the date_deadline or validity manually.
        """
        for record in self:
            if record.property_id and record.date_deadline:
                record.validity = (record.date_deadline - record.property_id.create_date.date()).days

    def action_accept(self):
        """Ensures that same offer is not accepted and Only one offer can be accepted per property!."""
        for record in self:
            if record.property_id.buyer_id == record.partner_id:
                raise UserError("You cannot accept your the same offer!")
            elif record.property_id.buyer_id:
                raise UserError("Only one offer can be accepted per property!")
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"

    def action_refuse(self):
        """Ensures an accepted offer cannot be refused!"""
        for record in self:
            if record.status == "accepted":
                raise UserError("An accepted offer cannot be refused!")
            record.status = "refused"
            if not record.property_id.offer_ids.filtered(lambda o: o.status == "accepted"):
                record.property_id.state = "offer_received"  # Fallback to previous state


    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        """Ensures that the selling price is at least 90% of the expected price unless it is zero."""
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                min_price = record.expected_price * 0.9
                if float_compare(record.selling_price, min_price, precision_digits=2) == -1:
                    raise models.ValidationError(
                        "The selling price cannot be lower than 90% of the expected price!"
                    )

    @api.model_create_multi
    def create(self, vals):
        """ Prevents creating an offer lower than an existing offer. """
        property_id = self.env["estate.property"].browse(vals["property_id"])

        # Check if there are existing offers and compare prices
        if property_id.offer_ids and vals["price"] <= max(property_id.offer_ids.mapped("price")):
            raise UserError("You cannot create an offer lower than an existing offer!")

        # Set property state to 'Offer Received'
        property_id.state = "offer_received"

        # Explicitly calling the parent class' create method
        return super(EstatePropertyOffer, self).create(vals)
