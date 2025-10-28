from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one(
        "estate.property", string="Property", required=True, ondelete="cascade"
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_state = fields.Selection(related="property_id.state")
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    _check_positive_offer_price = models.Constraint(
        "CHECK(price > 0)", "The Offer Price must be strictly positive"
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        self.ensure_one()
        for offer in self:
            offer.date_deadline = (
                offer.create_date or fields.Date.today()
            ) + relativedelta(days=+offer.validity)

    def _inverse_date_deadline(self):
        self.ensure_one()
        for offer in self:
            offer.validity = (
                offer.date_deadline - (offer.create_date or fields.Date.today()).date()
            ).days

    @api.model
    def create(self, vals_list):
        EstateProperties = self.env["estate.property"].with_prefetch(
            [vals["property_id"] for vals in vals_list]
        )
        for offer in vals_list:
            property = EstateProperties.browse(offer["property_id"])
            property.state = "offer_received"
            if offer["price"] < property.best_price:
                raise UserError(f"The offer must be higher than {property.best_price}")
        return super().create(vals_list)

    def action_accept_offer(self):
        self.ensure_one()
        for offer in self:
            if offer.status == "refused":
                raise UserError("You cannot accept a refused offer")
            if offer.property_id.buyer_id:
                raise UserError("Only one offer can be accepted")
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = "offer_accepted"
            offer.status = "accepted"
        return True

    def action_refuse_offer(self):
        self.ensure_one()
        for offer in self:
            if offer.status == "accepted":
                raise UserError("You cannot refuse an accepted offer")
            offer.status = "refused"
        return True
