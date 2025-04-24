from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", "Partner", required=True)
    property_id = fields.Many2one("estate.property", "Property", required=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date(
        "Deadline",
        compute="_compute_deadline",
        inverse="_inverse_deadline",
    )

    _sql_constraints = [
        (
            "check_price",
            "CHECK(price >= 0)",
            "An offer price must be strictly positive.",
        ),
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.date_deadline = base_date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_state_accept(self):
        for record in self:
            if record.property_id.offer_ids.filtered(lambda offer: offer.status == "accepted"):
                raise UserError("Only one offer can be accepted for a given property")
            record.status = "accepted"
            record.property_id.write(
                {
                    "selling_price": record.price,
                    "buyer_id": record.partner_id,
                }
            )
        return True

    def action_state_refuse(self):
        for record in self:
            record.status = "refused"
        return True
