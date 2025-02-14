from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"
    _order = "price desc"
    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "The offer price must be strictly positive",
        ),
    ]

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

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property_id = val["property_id"]
            if property_id:
                property = self.env["estate.property"].browse(property_id)
                if val["price"] < property.best_price:
                    raise UserError(f"The offer must be greater than {max}")
        offers = super().create(vals)
        for offer in offers:
            offer.property_id.status = "offer_received"
        return offers

    def action_accept(self):
        print(self.price)
        for record in self:
            if record.status == "accepted":
                raise UserError("This offer already accepted")

            other_offers = self.search(
                [
                    ("property_id", "=", record.property_id.id),
                    ("id", "!=", record.id),
                ],
                limit=1,
            )
            other_offers.write({"status": "refused"})
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.status = "offer_accepted"

    def action_refuse(self):
        for record in self:
            if record.status == "refused":
                raise UserError("This offer already refused")
            if record.status == "accepted":
                record.property_id.selling_price = 0
                record.property_id.buyer_id = False
                record.property_id.status = "offer_received"
            record.status = "refused"
