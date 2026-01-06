from typing import Required
from odoo import fields, models, api
from odoo.exceptions import UserError


class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "this is property offer model"

    price = fields.Float("price")
    status = fields.Selection(
        [("Accepted", "Accepted"), ("Refused", "Refused")], copy=False
    )
    validity = fields.Integer("validity", default=7)
    date_deadline = fields.Date(
        "date_deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("home.plan", required=True)

    _check_offer_price = models.Constraint(
        "CHECK( price > 0)", "The offer price must be Strictly positive"
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                record.create_date or fields.Date.today(), days=record.validity
            )

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_confirm(self):
        for record in self:
            if record.property_id.State == "Offer Accepted":
                raise UserError(message="You can't Accept multiple offer")
            else:
                record.status = "Accepted"
                record.property_id.Buyer = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.State = "Offer Accepted"

        return True

    def action_cancel(self):
        for record in self:
            record.status = "Refused"
        return True
