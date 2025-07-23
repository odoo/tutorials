from datetime import date, timedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price > 0)",
            "An offer price must be strictly positive.",
        )
    ]
    _order = "price desc"

    price = fields.Float("Offer Price")
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False)
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True, string="Property", readonly=True)
    date_deadline = fields.Date(
        "Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_deadline",
        store=True,
        readonly=False,
    )
    validity = fields.Integer("Validity (days)", default=7)

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            base_date = offer.create_date or date.today()

            offer.date_deadline = base_date + timedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            base_date = offer.create_date or date.today()

            if offer.date_deadline:
                offer.validity = (offer.date_deadline - base_date).days
            else:
                offer.validity = 7

    def accept(self):
        for offer in self:
            # if offer.property_id.state not in ('cancelled', 'sold','offer_accepted', 'new), same conditions for refusal
            offer.status = "accepted"
            offer.property_id.state = "offer_accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price

        return True

    def refuse(self):
        for offer in self:
            if offer.status != "accepted":
                offer.status = "refused"

        return True

    @api.model
    def create(self, vals):
        # self is empty before creation
        property = self.env["estate.property"].browse(vals["property_id"])
        property.state = "offer_received"

        if vals["price"] < max(property.offer_ids.mapped("price"), default=0.0):
            raise models.UserError("You can't add an offer wih a price lower than current best offer.")

        return super().create(vals)
