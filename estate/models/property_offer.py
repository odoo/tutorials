from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real estate property offers"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _check_expected_price_positive = models.Constraint(
        "CHECK(price > 0)",
        "Offer price must always be positive",
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.validity:
                crdate = record.create_date or fields.Date.today()
                record.date_deadline = crdate + relativedelta(
                    days=record.validity,
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = record._compute_validity()

    # inverse doesn't update the UI when date_deadline changes,
    # so we define an additional onchange to not confuse users
    @api.onchange("date_deadline")
    def _onchange_date_deadline(self):
        self.validity = self._compute_validity()

    def _compute_validity(self):
        crdate = fields.Date.today()
        if self.create_date:
            crdate = self.create_date.date()
        delta = self.date_deadline - crdate
        return delta.days

    def action_accept(self):
        # prevent accepting multiple offers
        if len(self) > 1:
            msg = "Only one offer can be accepted at a time"
            raise UserError(msg)

        # no need to process an already accepted offer
        if self.status == "accepted":
            return True

        # ensure no other offer is already accepted
        accepted_offers = [
            offer for offer in self.property_id.offer_ids if offer.status == "accepted"
        ]
        if len(accepted_offers) > 0:
            msg = "Another offer was already accepted"
            raise UserError(msg)

        self.status = "accepted"
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
