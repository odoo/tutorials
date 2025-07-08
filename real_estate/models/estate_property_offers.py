from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffers(models.Model):
    _name = "estate.property.offers"
    _description = "Estate Property Offers"
    _order = "price desc"

    price = fields.Float()
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    property_id = fields.Many2one(comodel_name="estate.property", required=True)
    validity = fields.Integer(default="7")
    property_type_id = fields.Many2one(
        related="property_id.estate_property_type_id", store=True
    )

    offer_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")]
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.offer_deadline = fields.Date.add(
                    record.create_date, days=record.validity
                )
            else:
                record.offer_deadline = fields.Date.add(
                    fields.Date.today(), days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.offer_deadline:
                record.validity = (
                    record.offer_deadline - fields.Date.to_date(record.create_date)
                ).days

    def action_accept_offer(self):
        for offer in self:
            accepted_offer = self.env["estate.property.offers"].search(
                [
                    ("property_id", "=", offer.property_id.id),
                    ("status", "=", "accepted"),
                ]
            )
            if accepted_offer:
                raise UserError("Only one offer can be accepted per property.")
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = "offer_accepted"

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"

    _sql_constraints = [
        (
            "check_offer_price_positive",
            "CHECK(price > 0)",
            "Offer price must be strictly positive.",
        )
    ]
