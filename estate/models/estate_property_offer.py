# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


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
