from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    price = fields.Float(string="Price")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")
            price = vals.get("price")

            if property_id and price:
                existing_offer = self.search(
                    [
                        ("property_id", "=", property_id),
                    ],
                    order="price desc",
                    limit=1,
                )

                if existing_offer and price < existing_offer.price:
                    raise ValidationError(
                        "You cannot create an offer lower than an existing offer."
                    )

        offers = super().create(vals_list)

        for offer in offers:
            if offer.property_id.state != 'offer_accepted':
                offer.property_id.state = "offer_received"

        return offers

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(
                fields.Date.to_date(create_date), days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.validity = (
                record.date_deadline - fields.Date.to_date(create_date)
            ).days

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
            record.property_id.state = "offer_accepted"

            other_offers = self.env["estate.property.offer"].search(
                [
                    ("property_id", "=", record.property_id.id),
                    ("id", "!=", record.id),
                ]
            )

            other_offers.write({"status": "refused"})

    def action_refuse(self):
        for record in self:
            record.status = "refused"

    def write(self, vals):
        result = super().write(vals)

        for offer in self:

            # If this offer is accepted and its price changes,
            # update the property's selling price.
            if offer.status == "accepted":
                offer.property_id.selling_price = offer.price
                offer.property_id.state = 'offer_accepted'

            if vals.get("status") == "accepted":
                other_offers = self.search([
                    ("property_id", "=", offer.property_id.id),
                    ("id", "!=", offer.id),
                ])

                other_offers.write({
                    "status": "refused",
                })

            if vals.get("status") == "refused":
                offers = self.search([
                    ("property_id", "=", offer.property_id.id),
                ])

                if all(offer.status == "refused" for offer in offers):
                    offer.property_id.state = "offer_received"
                    offer.property_id.selling_price = 0

        return result
