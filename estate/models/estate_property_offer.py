import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    create_date = fields.Date(default=datetime.date.today())
    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    validity = fields.Integer(default=7)
    deadline = fields.Date(compute="_compute_deadline", inverse="_compute_validity")
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    _check_price = models.Constraint(
        "CHECK(price > 0)",
    )

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            create_date = (
                record.create_date if record.create_date else datetime.date.today()
            )
            record.deadline = create_date + datetime.timedelta(days=record.validity)

    @api.depends("deadline", "create_date")
    def _compute_validity(self):
        for record in self:
            create_date = (
                record.create_date if record.create_date else datetime.date.today()
            )
            record.validity = (record.deadline - create_date).days

    def action_accept(self):
        for record in self:
            if record.status == "refused":
                raise UserError("A refused offer cannot be accepted")
            if record.property_id.state == "cancelled":
                raise UserError("An offer on a cancelled property cannot be accepted")
            if record.property_id.state == "sold":
                raise UserError("An offer on a sold property cannot be accepted")

            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("An accepted offer cannot be refused")
            if record.property_id.state == "cancelled":
                raise UserError("An offer on a cancelled property cannot be refused")
            if record.property_id.state == "sold":
                raise UserError("An offer on a sold property cannot be refused")

            record.status = "refused"
