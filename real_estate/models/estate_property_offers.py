# Part of Odoo. See LICENSE file for full copyright and licensing details.

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

    _sql_constraints = [
        (
            "check_offer_price_positive",
            "CHECK(price > 0)",
            "Offer price must be strictly positive.",
        )
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.offer_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.offer_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.offer_deadline:
                record.validity = (
                    record.offer_deadline - fields.Date.to_date(record.create_date)
                ).days

    def action_accept_offer(self):
        for offer in self:
            accepted_offer = offer.property_id.estate_property_offer_ids.filtered(
                lambda o: o.status == "accepted"
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

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property_id = self.env["estate.property"].browse(val["property_id"])

            if property_id.state == "sold":
                raise UserError("Cannot create an offer on a sold property.")

            if property_id.state == "new":
                property_id.state = "offer_received"

            if val["price"] <= property_id.best_offer:
                raise UserError(
                    f"The offer must be higher than {property_id.best_offer}"
                )
        return super().create(vals)
