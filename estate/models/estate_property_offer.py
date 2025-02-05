from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "These are all the offers for the property"

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline", inverse="_inverse_deadline"
    )

    _sql_constraints = [
        (
            "offer_price_positive",
            "check(price > 0)",
            "Offer price should be strictly positive.",
        )
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            creation_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(creation_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            creation_date = record.create_date.date()
            record.validity = (record.date_deadline - creation_date).days

    def accept_offer(self):
        for record in self:
            if not record.property_id.state == "offer_accepted":
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = "offer_accepted"
            else:
                raise UserError("An Offer has already been accepted.")

    def reject_offer(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.state = "offer_received"
            record.status = "refused"
