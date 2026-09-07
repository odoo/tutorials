from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    _order = "price desc"

    price = fields.Float()

    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
            ("sold", "Sold"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer")

    property_id = fields.Many2one("estate.property", string="Property")

    _check_price = models.Constraint(
    "CHECK(price >= 0)",
    "The offer price must be strictly positive.",
)

    validity = fields.Integer(default=7)

    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            if record.date_deadline:
                record.validity = (record.date_deadline - create_date).days

    def action_refuse(self):
        for record in self:
            record.status = "refused"

    def action_accept(self):
        for record in self:
            if "accepted" in record.property_id.offer_ids.mapped("status"):
                raise UserError("An offer has already been accepted for this property!")
            record.status = "accepted"
            other_offers = record.property_id.offer_ids - record
            other_offers.write({"status": "refused"})
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
