from odoo import models, fields, api
from odoo.tools.date_utils import relativedelta

PROPERTY_OFFER_STATE = [("accepted", "Accepted"), ("refused", "Refused")]


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(selection=PROPERTY_OFFER_STATE, copy=False)

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        "The offer price must be strictly positive."
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            base_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = base_date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            base_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - base_date).days

    def action_accept_offer(self):
        for offer in self:
            offer.status = "accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            for competing_offer in offer.property_id.offer_ids:
                if competing_offer != offer:
                    competing_offer.status = "refused"
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"
        return True
