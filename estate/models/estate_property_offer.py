from odoo import fields, models, api
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate offer"
    _order = "price desc"

    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "A property offer must be strictly positive.",
        ),
    ]

    price = fields.Float()
    status = fields.Selection(
        copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")]
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Buyer")
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_compute_validity", string="Deadline"
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            created_at = offer.create_date or fields.Date.today()
            offer.date_deadline = fields.Date.add(created_at, days=offer.validity)

    def _compute_validity(self):
        for offer in self:
            created_at = offer.create_date or fields.Date.today()
            delta = offer.date_deadline - created_at.date()
            offer.validity = delta.days

    def action_confirm(self):
        for offer in self:
            if offer.property_id.state in ["sold", "canceled"]:
                raise UserError("Property reached a final state")
            if offer.property_id.state == "offer_accepted":
                raise UserError("Cannot accept more than one offer")
            offer.status = "accepted"
            offer.property_id.state = "offer_accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
        return True

    def action_reject(self):
        for offer in self:
            if offer.property_id.state in ["sold", "canceled"]:
                raise UserError("Property reached a final state")
            if offer.status == "accepted":
                offer.property_id.state = "offer_received"
                offer.property_id.buyer_id = None
                offer.property_id.selling_price = 0
            offer.status = "refused"
        return True
