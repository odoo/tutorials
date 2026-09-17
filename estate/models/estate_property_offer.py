from datetime import datetime, timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer on a Real Estate Property"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )

    validity = fields.Integer("Validity (in days)", default=7)

    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    partner_id = fields.Many2one("res.partner", string="Made by", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    _check_price = models.Constraint("CHECK(price > 0)", "Offered price must be greater than zero")

    def action_accept_offer(self):
        for record in self:
            linked_property = record.property_id
            states = linked_property.offer_ids.mapped("status")

            if "accepted" in states:
                raise UserError(message="An offer was already accepted")

            if linked_property.state == "cancelled":
                raise UserError(message="Can't accept offers on cancelled auctions")

            record.status = "accepted"
            linked_property.selling_price = record.price
            linked_property.buyer_id = record.partner_id
            linked_property.state = "sold"

        return True

    def action_reject_offer(self):
        for record in self:
            record.status = "refused"

        return True

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            offer_date = record.create_date
            if not offer_date:
                offer_date = datetime.now()

            record.date_deadline = offer_date.date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            offer_date = record.create_date
            if not offer_date:
                offer_date = datetime.now()
            record.validity = (record.date_deadline - offer_date.date()).days
