from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        string="Status",
        copy=False
    )
    partner_ids = fields.Many2one(
        "res.partner",
        required=True,
    )
    property_ids = fields.Many2one("estate.property", required=True, ondelete="cascade")
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'Offer Price can be strictly positive'
    )
    _unique_partner_property = models.Constraint(
        "UNIQUE(property_ids, partner_ids)",
        "A partner can only submit one offer per property!"
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            start_date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            offer.date_deadline = fields.Date.add(
                start_date,
                days=offer.validity
            )

    def _inverse_date_deadline(self):
        for offer in self:
            start_date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )

            offer.validity = (offer.date_deadline - start_date).days

    def action_to_accept_offer(self):
        for offer in self:
            if "accepted" in offer.property_ids.offer_ids.mapped("status"):
                raise UserError("An Offer already is accepted")
            offer.status = "accepted"
            other_offer = offer.property_ids.offer_ids - offer
            other_offer.status = "refused"
            offer.property_ids.buyer_ids = offer.partner_ids
            offer.property_ids.selling_price = offer.price
            offer.property_ids.state = "offer_accepted"

    def action_to_reject_offer(self):
        self.status = "refused"
        return True
