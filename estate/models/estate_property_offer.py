# estate/models/estate_property_offer.py
from odoo import models, fields
from odoo import api
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"
    price = fields.Float(string="Offer Price")

    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)

    property_id = fields.Many2one("estate.property", string="Property", required=True)

    _sql_constraints = [
        (
            "check_offer_price_positive",
            "CHECK(price > 0)",
            "The offer price must be strictly positive.",
        ),
    ]

    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True,
        readonly=False,
    )

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            # Avoid crash on record creation (create_date might be False)
            create_dt = offer.create_date or fields.Datetime.now()
            offer.date_deadline = create_dt.date() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_dt = offer.create_date or fields.Datetime.now()
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - create_dt.date()).days

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.state == "sold":
                raise UserError("Cannot accept offers for a sold property.")
            # Refuse all other offers for the same property
            other_offers = offer.property_id.offer_ids - offer
            other_offers.write({"status": "refused"})

            offer.status = "accepted"
            offer.property_id.write(
                {
                    "buyer_id": offer.partner_id.id,
                    "selling_price": offer.price,
                    "state": "offer_accepted",
                }
            )
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"
        return True

    # @api.model
    # def create(self, vals):
    #     property_id = vals.get("property_id")
    #     amount = vals.get("price")

    #     if property_id and amount:
    #             property = self.env["estate.property"].browse(property_id)

    #     # Check for highest existing offer
    #     existing_offer = self.search([
    #         ('property_id', '=', property_id)
    #     ], order='price DESC', limit=1)

    #     if existing_offer and amount < existing_offer.price:
    #         raise UserError("You cannot offer less than an existing offer.")

    #     # Change property state to 'offer_received'
    #     property.write({"state": "offer_received"})

    #     return super().create(vals)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")
            amount = vals.get("price")

            if not (property_id and amount):
                continue

            property = self.env["estate.property"].browse(property_id)

            existing_offer = self.search(
                [("property_id", "=", property_id)], order="price DESC", limit=1
            )
            if existing_offer and amount < existing_offer.price:
                raise UserError("You cannot offer less than an existing offer.")
            property.state = "offer_received"

        return super().create(vals_list)
