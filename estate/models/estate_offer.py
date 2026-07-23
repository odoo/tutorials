from odoo import fields, models, api, exceptions
from datetime import timedelta

class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_dead_line", inverse="_inverse_validity")


    @api.depends("validity")
    def _compute_dead_line(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_validity(self):
        for offer in self:
            offer.validity = (offer.date_deadline - fields.Date.today()).days

    def action_accepte_offer(self):
        for offer in self:
            if offer.status =="refused":
                raise exceptions.UserError("Can't accept an refused offer")
            offer.status = "accepted"
            offer.property_id.accept_offer()
        return True

    def action_refuse_offer(self):
        for offer in self:
            if offer.status == "accepted":
                raise exceptions.UserError("Can't refuse an accepted offer")
            offer.status = "refused"
        return True
