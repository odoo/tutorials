from odoo import fields, models, api
from odoo.exceptions import UserError
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
    date_deadline = fields.Date(
        string="Date Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    _sql_constraints = [
        ("positive_offer_price", "CHECK(price > 0)",
         "A property offer price must be strictly positive.")
    ]

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
        """Ensures that only one offer can be accepted per property and other offers are refused."""
        for record in self:
            # Check if the same partner is trying to accept their own offer
            if record.property_id.buyer_id == record.partner_id:
                raise UserError("You cannot accept your own offer!")
            # Check if another offer has already been accepted for this property
            elif record.property_id.buyer_id:
                raise UserError("Only one offer can be accepted per property!")

            # Accept the current offer
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"

            # Refuse all other offers for the same property
            other_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', record.property_id.id),
                ('id', '!=', record.id)  # Exclude the current accepted offer
            ])
            for offer in other_offers:
                offer.status = "refused"  # Refuse the other offers

    def action_refuse(self):
        """Ensures an accepted offer cannot be refused!"""
        for record in self:
            if record.status == "accepted":
                raise UserError("An accepted offer cannot be refused!")
            record.status = "refused"
            if not record.property_id.offer_ids.filtered(lambda o: o.status == "accepted"):
                record.property_id.state = "offer_received"  # Fallback to previous state

    @api.model_create_multi
    def create(self, vals_list):
        """Prevents creating an offer lower than an existing offer."""
        for vals in vals_list:  # Loop added
            property_id = self.env["estate.property"].browse(vals.get("property_id"))

            if not property_id:
                raise UserError("Property must be specified for an offer.")
            if property_id.offer_ids and vals["price"] <= max(property_id.offer_ids.mapped("price")):
                raise UserError("You cannot create an offer lower than an existing offer!")

            property_id.state = "offer_received"

        return super(EstatePropertyOffer, self).create(vals_list)
