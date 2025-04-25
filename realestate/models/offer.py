from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError


class Offer(models.Model):
    _name = "offer"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")])
    buyer_id = fields.Many2one("buyer")
    property_id = fields.Many2one("realestate")
    validity = fields.Integer()
    deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.deadline = (
                record.create_date or fields.Datetime.now()
            ).date() + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (
                record.deadline - (record.create_date or fields.Datetime.now()).date()
            ).days

    def set_offer_accepted(self):
        self.ensure_one()
        record = self
        for record in self:
            if record.property_id.state == "sold":
                raise UserError("This property is already sold")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.owner_id = record.buyer_id
            record.property_id.buyer_id = record.property_id.owner_id
            record.property_id.state = "sold"

            # record.property_id.owner_id = record.buyer_id

    def set_offer_refused(self):
        for record in self:
            self.status = "refused"
            record.property_id.selling_price = 0

    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price> 0)",
            "Offer price must be positive.",
        )
    ]
