import datetime
from datetime import timedelta

from odoo.exceptions import UserError

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer"
    price = fields.Float()
    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The offered price must be strictly positive.",
    )
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    date_deadline = fields.Date(
        compute="_compute_deadline", inverse="_inverse_deadline"
    )

    validity = fields.Integer(default=7)

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = (
                record.create_date or fields.Date.today()
            ) + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            creation_date: datetime.datetime = (
                record.create_date or fields.Datetime.today()
            )
            record.validity = (
                record.date_deadline - creation_date.date()
            ) // timedelta(days=1)

    def accept(self):
        for record in self:
            if not record.property_id.buyer_id:
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
            else:
                raise UserError("The property already have a buyer defined")

    def refuse(self):
        for record in self:
            record.status = "refused"
