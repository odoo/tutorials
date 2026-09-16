from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

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
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )
    validity = fields.Integer(default=7)

    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be strictly positive.",
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

    @api.model
    def create(self, vals):
        offer = super().create(vals)
        if offer.property_id.state == "new":
            offer.property_id.state = "offer_received"
        return offer

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
        if any(offer.status == "accepted" for offer in self.property_id.offer_ids):
            raise UserError(_("Only one offer can be accepted."))
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = "offer_accepted"

    def action_refuse(self):
        self.status = "refused"
        self.property_id.state = "offer_received"
