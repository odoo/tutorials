from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            start_date = (
                offer.create_date.date() if offer.create_date else fields.Date.context_today(offer)
            )
            offer.date_deadline = fields.Date.add(start_date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            start_date = (
                offer.create_date.date() if offer.create_date else fields.Date.context_today(offer)
            )
            offer.validity = (offer.date_deadline - start_date).days

    def action_accept(self):
        for offer in self:
            if offer.property_id.state == "sold" or offer.property_id.state == "offer_accepted":
                raise UserError(self.env._("An offer had already been accepted."))
            if offer.property_id.state == "cancelled":
                raise UserError(self.env._("The sales had been cancelled."))
            offer.status = "accepted"
            offer.property_id.state = "offer_accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
        return True

    def action_refuse(self):
        for offer in self:
            if offer.property_id.state == "sold" or offer.property_id.state == "cancelled":
                return True
            offer.status = "refused"
        return True
