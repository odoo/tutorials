from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    _check_negative_offer_price = models.Constraint(
        "CHECK(price >= 0)",
        "Have you ever thought of having negative value as an offer Price? Price can't be negative, check your Math!",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    @api.constrains("price")
    def _check_offer_price(self):
        for record in self:
            if float_compare(record.price, (record.property_id.expected_price) * 0.9, precision_digits=2) == -1:
                raise UserError("You cannot enter Offer Price less than 90% of Property Expected Price")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env["estate.property"].browse(vals["property_id"])
            if vals["price"] < property.best_offer:
                raise UserError("You cannot create an offer having less amount than an existing price.")
            if property.state != "offer_received":
                property.state = "offer_received"
        return super().create(vals_list)

    def action_accept(self):
        if "accepted" in self.property_id.offer_ids.mapped("status"):
            raise UserError("You cannot accept more than 1 offer for a single Property")
        for record in self:
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
