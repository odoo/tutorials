# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float()
    state = fields.Selection(
        string="State",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        help="State of the offer",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.estate_type_id", store=True
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline", inverse="_inverse_deadline"
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(
                    record.create_date, days=record.validity
                )
            else:
                record.date_deadline = fields.Date.add(
                    fields.Date.today(), days=record.validity
                )

    def _inverse_deadline(self):
        for record in self:
            diff = int((record.date_deadline - fields.Date.today()).days)
            record.validity = diff

    _check_offer_price_positive = models.Constraint(
        "CHECK(price > 0)", "The offer price must be positive."
    )

    def action_accept_offer(self):
        for record in self:
            record.state = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "sold"

            for offer in record.property_id.offer_ids:
                if offer.id != record.id:
                    offer.state = "refused"
        return True

    def action_refuse_offer(self):
        for record in self:
            record.state = "refused"
        return True

    @api.model
    def create(self, vals_list):
        current_property = self.env["estate.property"].browse(
            vals_list[0]["property_id"]
        )
        if current_property.state not in {"new", "offer_received"}:
            error_message = (
                "The sale is closed and no offer can be added for this property"
            )
            raise ValidationError(error_message)
        current_offers = current_property.offer_ids
        if len(current_offers) > 0:
            best_offer_price = max(offer.price for offer in current_offers)
            feedback_buffer = []
            for new_offer in vals_list:
                if new_offer["price"] < best_offer_price:
                    feedback_buffer.append(str(new_offer["price"]))
            if len(feedback_buffer) > 0:
                error_message = (
                    f"The following offer prices are lower than the current best price ({best_offer_price}) and can't therefor not be added:\n - "
                    + "\n - ".join(feedback_buffer)
                )
                raise ValidationError(error_message)
        current_property.state = "offer_received"
        return super().create(vals_list)
