from odoo import fields, models, api, exceptions, tools
from datetime import timedelta


class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Offer"
    _order = "price desc"

    price = fields.Float(string="Offer Price")
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
        string="Status",
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline", inverse="_inverse_deadline"
    )

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date.date() + timedelta(
                    days=offer.validity
                )
            else:
                offer.date_deadline = fields.Date.today() + timedelta(
                    days=offer.validity
                )

    def _inverse_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            else:
                offer.validity = (offer.date_deadline - fields.Date.today()).days

    def set_status_accepted(self):
        for offer in self:
            if not offer.property_id.has_accepted_offer:
                offer.status = "accepted"
                if offer.property_id.state not in [
                    "offer Accepted",
                    "sold",
                    "cancelled",
                ]:
                    offer.property_id.state = "offer Accepted"
            else:
                raise exceptions.UserError(("You can't accept multiple offers"))
        return True

    def set_status_refused(self):
        for offer in self:
            offer.status = "refused"
        return True

    _check_offer_price = models.Constraint(
        "CHECK(price > 0)",
        "The price of an offer needs to be strictly positive",
    )

    @api.constrains("status", "price")
    def _check_selling_price(self):
        for offer in self:
            if offer.status != "accepted":
                return True

            if (
                tools.float_compare(
                    (offer.property_id.expected_price * 0.9), offer.price, 2
                )
                >= 0
            ):
                raise exceptions.ValidationError(
                    "The selling price cant be lower than 90 percent of the expected price"
                )
