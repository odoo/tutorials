from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "its for the offers that we recive in the estate"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, readonly=True)
    validity = fields.Integer(default=7)

    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            base_date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            offer.date_deadline = fields.Date.add(
                base_date,
                days=offer.validity,
            )

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                base_date = (
                    offer.create_date.date()
                    if offer.create_date
                    else fields.Date.today()
                )
                offer.validity = (offer.date_deadline - base_date).days

    def action_accept(self):
        if "accepted" in self.property_id.offer_ids.mapped("status"):
            raise UserError("Only one offer can be accepted for a property.")
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = "offer_accepted"

    def action_refuse(self):
        self.status = "refused"

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be strictly positive.",
    )
