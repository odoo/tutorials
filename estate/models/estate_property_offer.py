from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_state = fields.Selection(related="property_id.state", string="Property State")
    # A related field must have the same type as the field it points to.
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _check_price_positive = models.Constraint(
        "CHECK(price > 0)",
        "An offer price must be strictly positive.",
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            start_date = (
                offer.create_date.date() if offer.create_date else fields.Date.context_today(offer)
            )
            offer.date_deadline = fields.Date.add(start_date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            start_date = (
                offer.create_date.date() if offer.create_date else fields.Date.context_today(offer)
            )
            offer.validity = (offer.date_deadline - start_date).days

    def action_accept(self):
        for offer in self:
            if offer.property_id.state in {"sold", "offer_accepted"}:
                raise UserError(self.env._("An offer had already been accepted."))
            if offer.property_id.state == "cancelled":
                raise UserError(self.env._("The sales had been cancelled."))
            offer.status = "accepted"
            offer.property_id.state = "offer_accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
        return True

    def action_refuse(self):
        for offer in self:
            if offer.property_id.state not in {"sold", "cancelled"}:
                offer.status = "refused"
        return True

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            # Instantiate an estate.property object
            estate = self.env["estate.property"].browse(vals["property_id"])
            if estate.state in {"cancelled", "sold"}:
                raise ValidationError(self.env._("You cannot make an offer on this property anymore."))
            if estate.state == "new":
                estate.state = "offer_received"
            best_offer = max(estate.offer_ids.mapped("price"), default=0.0)
            if vals.get("price", 0.0) < best_offer:
                raise ValidationError(self.env._(f"The offer must be higher than {best_offer:,.2f}."))
        return super().create(vals_list)
