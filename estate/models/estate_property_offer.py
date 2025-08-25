from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be greater than 0."),
    ]
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    validity = fields.Integer(
        string="Validity(days)",
        default=7,
        help="Validity of the offer in days, after that it will be refused automatically.",
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            base_date = (
                fields.Date.to_date(offer.create_date)
                if offer.create_date
                else fields.Date.context_today(offer)
            )
            offer.date_deadline = base_date + timedelta(days=offer.validity or 0)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                base_date = (
                    fields.Date.to_date(offer.create_date)
                    if offer.create_date
                    else fields.Date.context_today(offer)
                )
                offer.validity = (offer.date_deadline - base_date).days
            else:
                offer.validity = 0

    @api.model_create_multi
    def create(self, vals_list):
        for record in vals_list:
            property = self.env["estate.property"].browse(record["property_id"])

            if record.get("price") < property.best_price:
                raise UserError(
                    "You cannot create an offer lower than an existing one."
                )

            property.state = "offer received"
        return super().create(vals_list)

    def action_set_accepted(self):
        for offer in self:
            if offer.property_id.selling_price == 0.0:
                offer.write({"status": "accepted"})

                offer.property_id.write(
                    {
                        "state": "offer accepted",
                        "selling_price": offer.price,
                        "buyer_id": offer.partner_id.id,
                    }
                )

                other_offers = offer.property_id.offer_ids - offer

                other_offers.write({"status": "refused"})
            else:
                raise UserError("One offer is already accepted for this property.")

    def action_set_refused(self):
        for offer in self:
            if offer.status == "accepted":
                offer.property_id.state = "offer received"
                offer.property_id.buyer_id = False
                offer.property_id.selling_price = 0.0
            offer.status = "refused"
