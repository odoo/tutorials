from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    validity = fields.Integer(
        default=7,
    )
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property",
        required=True,
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True,
    )
    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'Offer Price must be strictly positive.',
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            create_date = (
                offer.create_date.date()
                if offer.create_date
                else fields.Date.today()
            )
            offer.date_deadline = (
                create_date +
                timedelta(days=offer.validity)
            )

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = (
                offer.create_date.date()
                if offer.create_date
                else fields.Date.today()
            )
            if offer.date_deadline:
                offer.validity = (
                    offer.date_deadline -
                    create_date
                ).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")
            price = vals.get("price")
            if property_id and price:
                property = self.env["estate.property"].browse(property_id)
                for offer in property.offer_ids:
                    if price < offer.price:
                        raise UserError(
                            "The offer must be higher than existing offers."
                        )
        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.state == "new":
                offer.property_id.state = "offer_received"
        return offers

    def action_accept(self):
        for offer in self:
            if offer.property_id.offer_ids.filtered(
                lambda o: o.status == "accepted" and o.id != offer.id
            ):
                raise UserError(
                    "Another offer for this property has already been accepted."
                )
            offer.status = "accepted"
            offer.property_id.write({
                "buyer_id": offer.partner_id.id,
                "selling_price": offer.price,
                "state": "offer_accepted",
            })
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True
