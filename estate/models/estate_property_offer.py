from datetime import date

from odoo import fields, models, api, _
from odoo.tools import date_utils
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers made on a listing"
    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "Price of an offer should be only positive",
        ),
    ]
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline",
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            create_date_actual = (
                date.today() if not offer.create_date else offer.create_date.date()
            )
            offer.date_deadline = date_utils.add(
                create_date_actual, days=offer.validity
            )

    def _inverse_date_deadline(self):
        for offer in self:
            create_date_actual = (
                date.today() if not offer.create_date else offer.create_date.date()
            )
            offer.validity = (offer.date_deadline - create_date_actual).days

    def action_offer_accept(self):
        for offer in self:
            offer.status = "accepted"
            if self.property_id.state in ("offer-accepted", "sold"):
                self.status = False
                raise UserError(_("An offer has already been accepted!"))
            else:
                self.property_id.write({"state": "offer-accepted", "selling_price": self.price, "buyer_id": self.partner_id})
        return True

    @api.depends("status")
    def action_offer_refuse(self):
        self.status = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            single_property = self.env["estate.property"].browse(vals["property_id"])
            price = vals.get("price")
            if price is not None and price < single_property.best_price:
                raise UserError(_("An offer cannot be lower than an existing offer"))
            single_property.state = "offer-received"
        return super().create(vals_list)
