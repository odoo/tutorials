from odoo.exceptions import UserError

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for property"
    _order = "price desc"

    price = fields.Float()
    state = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.estate_property_type_id",
        store=True,
    )

    _check_offer_price_positive = models.Constraint(
        "CHECK(price > 0)", "The offer price must be positive."
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = fields.Date.add(
                    offer.create_date,
                    days=offer.validity,
                )
            else:
                offer.date_deadline = fields.Date.add(
                    fields.Date.today(), days=offer.validity
                )

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            else:
                offer.validity = (offer.date_deadline - fields.Date.today()).days

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.buyer_id:
                raise UserError(
                    "a buyer is already assigned , therefore another offer has been accepted"
                )
            offer.state = "accepted"
            offer.property_id.selling_price = self.price
            offer.property_id.buyer_id = self.partner_id

        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.state = "refused"
        return True

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            higher_offer = self.search_count(
                [
                    ("property_id.id", "=", vals["property_id"]),
                    ("price", ">", vals["price"]),
                ],
                1,
            )
            if higher_offer:
                raise UserError("Can't create an offer with a lower price")

            self.env["estate.property"].browse(
                vals["property_id"]
            ).state = "offer_received"

        return super().create(vals_list)
