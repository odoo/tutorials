from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date(
        "Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    _check_price = models.Constraint(
        "CHECK (price > 0)",
        "An offer price must be strictly positive",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (
                record.create_date or fields.Datetime.now()
            ).date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                date_diff = record.date_deadline - record.create_date.date()
                record.validity = date_diff.days

    @api.model
    def create(self, vals_list):
        property_ids = {
            vals.get("property_id") for vals in vals_list if vals.get("property_id")
        }
        properties = self.env["estate.property"].browse(property_ids)
        properties_by_id = {property.id: property for property in properties}

        for vals in vals_list:
            property = properties_by_id.get(vals.get("property_id"))
            price = vals.get("price", 0)

            if property and price < property.best_price:
                raise ValidationError(
                    self.env._("You cannot create offer lower than an existing offer.")
                )

        offers = super().create(vals_list)

        properties = offers.mapped("property_id").filtered(lambda p: p.state == "new")
        if properties:
            properties.write({"state": "offer_received"})

        return offers

    def action_offer_accept(self):
        self.ensure_one()
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.status = "accepted"
        self.property_id.state = "offer_accepted"

        existing_offers = self.property_id.offer_ids.filtered(
            lambda offer: offer.id != self.id
        )
        if existing_offers:
            existing_offers.status = 'refused'

    def action_offer_reject(self):
        self.ensure_one()
        self.status = "refused"
