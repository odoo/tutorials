from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
        string="Status",
    )
    partner_id = fields.Many2one("res.partner", string="partner", required=True)
    property_id = fields.Many2one(
        "estate.property", string="property", required=True, ondelete="cascade"
    )

    validity = fields.Integer(default=7, string="validity (days)")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    _check_offer_price = models.Constraint(
        "check(price > 0 )", "The offer Price should be Positive. "
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = (
                offer.create_date.date() if offer.create_date else fields.date.today()
            )
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - date).days

    def action_accept(self):
        for offer in self:
            if "accepted" in offer.property_id.offer_ids.mapped("status"):
                raise UserError(
                    "An offer has already been accepted for this property!!!!"
                )

            offer.status = "accepted"

            offer.property_id.state = "offer_accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            other_offers = offer.property_id.offer_ids.filtered(
                lambda o: o.id != offer.id
            )
            other_offers.status = "refused"
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
            offer.property_id.state = "new"
            if offer.property_id.buyer_id == offer.partner_id:
                offer.property_id.buyer_id = False
                offer.property_id.selling_price = 0
        return True
