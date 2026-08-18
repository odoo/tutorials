from odoo import models, fields, api, exceptions
from datetime import timedelta

import logging

_logger = logging.getLogger(__name__)


class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float("Offer Price")
    state = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner = fields.Many2one(string="Buyer", comodel_name="res.partner", required=True)
    property = fields.Many2one(comodel_name="estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date("Offer Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    _price_strictly_positive = models.Constraint(
        'CHECK(price > 0)',
        'Offer price must be strictly positive'
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for offer in self:
            compare_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = compare_date + timedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def action_accept_offer(self):
        # We can only accept one offer at a time
        self.ensure_one()

        # Ensure there is no existing accepted offer
        for offer in self.property.offers:
            if offer.state == "accepted":
                raise exceptions.UserError("Property already has an accepted offer.")

        self.state = "accepted"

        self.property.buyer = self.partner
        self.property.selling_price = self.price

        return True

    def action_refuse_offer(self):
        for offer in self:
            # We could forbid refusing accepted offers
            offer.state = "refused"
        return True
