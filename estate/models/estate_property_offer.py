from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An offer for an estate property"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    _check_offer_price = models.Constraint(
        "CHECK(price > 0)",
        "An offer price must be strictly positive.",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            delta = record.date_deadline - record.create_date.date()
            record.validity = delta.days

    def action_accept(self):
        for record in self:
            if record.property_id.offer_ids.filtered(lambda offer: offer.status == "accepted"):
                raise UserError("There is already an accepted offer for this property.")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
