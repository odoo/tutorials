from odoo import _, api, exceptions, fields, models
from datetime import timedelta
from odoo.tools.float_utils import float_compare
from odoo.exceptions import ValidationError, UserError


class RealEstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_set_deadline")
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )

    _check_offer_price = models.Constraint(
        "CHECK(price > 0)", "The offer price should be strictly positive."
    )

    def _set_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for record in self:
            if record.property_id.state in ["sold", "canceled"]:
                raise exceptions.UserError(
                    "You cannot accept an offer on a sold or canceled property."
                )
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"

    def action_refuse(self):
        self.status = "refused"

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env["estate.property"].browse(vals["property_id"])
            if property:
                if property.state == "new":
                    property.state = "offer_received"

                if vals["price"] < property.best_offer:
                    raise UserError(
                        _("Offer must be higher or equal than %d", property.best_offer)
                    )

        return super().create(vals_list)
    
    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = fields.Date.today() + timedelta(
                    days=record.validity
                )

    @api.constrains("price")
    def _check_selling_price(self):
        for record in self:
            if (
                float_compare(
                    record.price, (record.property_id.expected_price * 0.9), 2
                )
                < 0
            ):
                raise ValidationError(
                    _(
                        "The best offer must be at least 90% of the expected price to accept an offer."
                    )
                )

