from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        (
            "check_estate_property_offer_price",
            "CHECK(price > 0)",
            "Offer Price must be a strictly positive amount",
        )
    ]
    # --------------------------------------- Fields Declaration ----------------------------------
    # Basic
    price = fields.Float(required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    state = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
        default=False,
    )
    # Relational
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    # ---------------------------------------- Compute methods ------------------------------------
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    # For making manual changes in computed fields.
    def _inverse_date_deadline(self):
        for offer in self:
            date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            offer.validity = (offer.date_deadline - date).days
    # ---------------------------------------- Offer's Action Method -------------------------------------
    def offer_accept(self):
        if self.state == "accepted":
            raise UserError("This offer has already been accepted")
        self.state = "accepted"
        self.property_id.state = "offer_accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id

        for offer in self.property_id.offer_ids:
            if offer.id != self.id:
                offer.state = "refused"

    def offer_refuse(self):
        for offers in self:
            if offers.state == "refused":
                raise UserError("This offer has already been refused")
            offers.state = "refused"
            self.property_id.state = "cancelled"
            offers.property_id.selling_price = None
            offers.property_id.buyer_id = None
        return True
    # ------------------------------------------ CRUD Methods ------------------------------------
    @api.model
    def create(self, vals):
        property = self.env["estate.property"].browse(vals.get("property_id"))

        existing_offers = self.search([("property_id", "=", property.id)])
        if existing_offers:
            max_offer_price = max(existing_offers.mapped("price")) 
            if vals.get("price") <= max_offer_price:
                new_price = max_offer_price - vals.get("price") + 1
                raise UserError(
                    f"You cannot create an offer lower than an existing offer. "
                    f"Please add at least {new_price} more to create a new offer!"
                )
        property.state = "offer_received"
        return super(EstatePropertyOffer, self).create(vals)
