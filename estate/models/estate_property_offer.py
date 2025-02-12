from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "The offer price must be strictly positive",
        ),
    ]

    @api.depends("validity", "property_id")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                fields.Date.today(), days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                create_date = (
                    record.create_date.date()
                    if record.create_date
                    else fields.Date.today()
                )
                record.validity = (record.date_deadline - create_date).days

    @api.constrains("price", "status")
    def _check_price(self):
        for record in self:
            if (
                record.price < ((record.property_id.expected_price * 90) / 100)
                and record.status == "accepted"
            ):
                raise ValidationError(
                    "The selling price must be atleast 90% of the expected price! You must reduce expected price if you want to accept this offer."
                )

    def accept_offer(self):
        print(self.price)
        for record in self:
            if record.status == "accepted":
                raise UserError("This offer already accepted")

            other_offers = self.search(
                [
                    ("property_id", "=", record.property_id.id),
                    ("id", "!=", record.id),
                ]
            )
            other_offers.write({"status": "refused"})
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.status = "offer_accepted"

    def refuse_offer(self):
        for record in self:
            if record.status == "refused":
                raise UserError("This offer already refused")
            if record.status == "accepted":
                record.property_id.selling_price = 0
                record.property_id.buyer_id = False
                record.property_id.status = "offer_received"
            record.status = "refused"

    @api.model_create_multi
    def create(self, vals_list):
        max = 0
        for val in vals_list:
            property_id = val.get("property_id")
            if property_id:
                property = self.env["estate.property"].browse(property_id)
                for offer in property.offer_ids:
                    if offer.price > max:
                        max = offer.price
                if val.get("price") < max:
                    raise UserError(f"The offer must be greater than {max}")
        offers = super().create(vals_list)
        for offer in offers:
            offer.property_id.status = "offer_received"
        return offers
