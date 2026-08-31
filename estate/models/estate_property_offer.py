from odoo import api, exceptions, fields, models
from odoo.tools import _


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float("Price")
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, readonly=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    _check_offer_price = models.Constraint(
        'CHECK(price >= 0)',
        'The offer price must be greater than zero (0)',
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                fields.Date.today(),
                days=record.validity,
            )

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    def refuse_offer(self):
        for record in self:
            record.status = "refused"

    def accept_offer(self):
        for record in self:
            estate_property = record.property_id
            accepted_offer = estate_property.offer_ids.filtered(
                lambda offer: offer.status == "accepted"
            )
            if accepted_offer:
                raise exceptions.UserError(_(
                    "This property already has an accepted offer."
                ))

            record.status = "accepted"

            estate_property.buyer_id = record.partner_id
            estate_property.selling_price = record.price
            estate_property.seller_id = self.env.user
