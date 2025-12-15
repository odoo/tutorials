from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        compute="_compute_deadline", inverse="_inverse_deadline", string="Deadline",
    )

    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Property")
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True,
    )

    _check_positive_price = models.Constraint(
        "CHECK(price > 0)",
        "The expected price of a offer must be positive.",
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = fields.Date.add(
                    offer.create_date, days=offer.validity,
                )
            else:
                offer.date_deadline = fields.Date.add(
                    fields.Date.today(), days=offer.validity,
                )

    def _inverse_deadline(self):
        for offer in self:
            offer.validity = (
                offer.date_deadline - fields.Date.to_date(offer.create_date)
            ).days

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.state == "offer_accepted":
                offer.status = "refused"
                return True
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = "offer_accepted"
        return True

    def action_refuse_offer(self):
        for offer in self:
            if offer.status == "accepted":
                offer.property_id.selling_price = 0
                offer.property_id.buyer_id = ""
            offer.status = "refused"
        return True

    @api.model
    def create(self, vals):
        for record in vals:
            best_price = self.env["estate.property"].browse(record["property_id"]).best_price
            if record["price"] < best_price:
                raise ValidationError(self.env._("The offer must be greater than %s€", best_price))
        return super().create(vals)
