from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError


class Offer(models.Model):
    _name = "offer"
    _order = "price desc"
    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")])
    buyer_id = fields.Many2one("res.partner")
    property_id = fields.Many2one("realestate")
    property_type_id = fields.Many2one(related="property_id.type_id")
    state = fields.Selection(related="property_id.state")
    validity = fields.Integer()
    deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    highest_offer = fields.Float(compute="_calc_highest_price")

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
        for record in self:
            if record.property_id.state == "sold":
                raise UserError("This property is already sold")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.buyer_id
            record.property_id.state = "offer_accepted"

    def set_offer_refused(self):
        for record in self:
            if record.property_id.state == "sold":
                raise UserError("This property is already sold")
            self.status = "refused"

    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price> 0)",
            "Offer price must be positive.",
        )
    ]

    def create(self, vals):
        res = super(Offer, self).create(vals)

        if res.price < res.property_id.best_price:
            raise UserError("Please set a higher price!")
        return res
