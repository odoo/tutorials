from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"
    _order = "price desc"
    _sql_constraints = [("price_pos", "check(price>0)", "price should be positive!")]

    price = fields.Float()
    state = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "refused")]
    )
    validity = fields.Integer(default=7)
    deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_deadline", store=True
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.deadline = record.create_date.date() if record.create_date else fields.date.today() + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.create_date and record.deadline:
                record.validity = (record.deadline - record.create_date.date()).days

    @api.model
    def create(self, vals):
        property = self.env['estate.property'].browse(vals.get('property_id'))
        if property.offer_ids:
            if vals.get('price') < property.best_offer:
                raise ValidationError("The offer price should be more than best offer")
        property.status = "offer_received"
        return super().create(vals)

    def action_offer_accept(self):
        for record in self:
            if record.state == "accepted":
                raise UserError("Offer is already accepted")
            else:
                record.property_id.write(
                    {
                        "buyer_id": record.partner_id.id,
                        "selling_price": record.price,
                        "status": "offer_accepted",
                    }
                )
                record.state = "accepted"
                other_offer = record.property_id.offer_ids.filtered(lambda offer: record.id != offer.id)
                other_offer.write({"state": "refused"})

    def action_offer_reject(self):
        for record in self:
            if record.state == "refused":
                raise UserError("Offer is already refused")
            else:
                record.state = "refused"
                record.property_id.write({"selling_price": False, "buyer_id": False})
