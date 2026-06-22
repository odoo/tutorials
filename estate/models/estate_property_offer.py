from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(
        string="Deadline Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        required=True,
    )
    property_id = fields.Many2one(
        comodel_name="estate.property",
        string="Property",
        required=True,
    )
    property_type_id = fields.Many2one(
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )

    _check_price_positive = models.Constraint(
        "CHECK(price > 0)",
        "An offer price should be strictly positive.",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Datetime.now()
            offer.date_deadline = create_date.date() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Datetime.now()
            offer.validity = (offer.date_deadline - create_date.date()).days

    @api.model
    def create(self, vals_list):
        properties = self.env["estate.property"].browse(
            [vals["property_id"] for vals in vals_list]
        )

        for vals in vals_list:
            property = properties.browse(vals["property_id"])

            if property.state == "sold":
                raise UserError(
                    self.env._("You can't create an offer for a sold property.")
                )

            if vals["price"] < property.best_price:
                raise UserError(
                    self.env._(
                        "You can't create an offer with a lower amount than an "
                        "existing offer."
                    )
                )

            property.state = "offer_received"

        return super().create(vals_list)

    def action_accept_offer(self):
        self.ensure_one()

        if self.status == "accepted":
            raise UserError(self.env._("You already accepted the offer."))

        if self.property_id.buyer_id:
            raise UserError(self.env._("Only one offer can be accepted."))

        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = "offer_accepted"
        self.property_id.offer_ids.filtered(lambda offer: offer != self).status = (
            "refused"
        )

        return True

    def action_refuse_offer(self):
        self.ensure_one()

        if self.status == "accepted":
            raise UserError(
                self.env._("You cannot refuse an offer once it has been accepted.")
            )

        self.status = "refused"
        return True
