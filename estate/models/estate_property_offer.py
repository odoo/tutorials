from datetime import timedelta

from odoo import api, exceptions, fields, models
from odoo.exceptions import UserError

class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused"),
    ], string="Status")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (Days)", default=7)
    date_deadline = fields.Date(
        string="Deadline", 
        compute="_compute_date_deadline", 
        inverse="_inverse_date_deadline", 
        store=True
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )
    
    #constraint
    _sql_constraints = [
        ("check_offer_price", "CHECK(price >0)", "The offer price must be strictly more than zero."),
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        """Compute the date_deadline based on create_date and validity."""
        for offer in self:
            if offer.create_date:  # Ensure create_date is not None
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        """Set the validity field based on date_deadline."""
        for offer in self:
            if offer.create_date and offer.date_deadline:
                delta = (offer.date_deadline - offer.create_date.date()).days
                offer.validity = delta

    def accept_offer(self):
        for offer in self:
            # Check if the property is already sold
            if offer.property_id.state in ["sold","offer_accepted"]:
                raise UserError("This property has already been sold or accepted offer.")
            # Set the offer status to accepted and the property state to sold
            offer.status = "accepted"
            offer.property_id.state = "offer_accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price

    def refuse_offer(self):
        for offer in self:
            if offer.property_id.state == "sold":
                raise UserError("You cannot refuse the offer on sold properties.")
            offer.status = "refused"    
            offer.property_id.state = "offer_received"
            offer.property_id.selling_price = False
            offer.property_id.buyer_id = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env["estate.property"].browse(vals["property_id"])
            if property.state == 'sold':
                raise UserError("You cannot create an offer for a sold property.")
            if property.expected_price > vals['price']:
                raise ValidationError(
                    "You cannot create an offer lower than expected price."
                )
            for offer in property.offer_ids:
                if offer.price > vals["price"]:
                    raise UserError("The offer must be higher than the existing offer")
            property.state = "offer_received"
        return super().create(vals_list)

    @api.model
    def unlink(self):
        properties = self.mapped("property_id")
        result = super(estatePropertyOffer, self).unlink()
        # Check each property and update its state if it has no more offers
        for property in properties:
            if not property.offer_ids:
                property.state = "new"
        return result    
            