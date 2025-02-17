# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be strictly positive"),
    ]

    price = fields.Float("Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)

    state = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status", copy=False
    )

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", string="Property Type", store=True)

    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    @api.model_create_multi
    def create(self, vals_list):
        for offer in vals_list:
            property = self.env["estate.property"].browse(offer["property_id"])
            if property.state == "sold":
                raise UserError(_("You can not create an offer for a sold property"))
            if property.state != "offer_received":
                property.state = "offer_received"
            if property.offer_ids:
                max_offer = max(property.offer_ids.mapped("price"))
                max_offer_partner_name = property.offer_ids.filtered(lambda x: x.price == max_offer).mapped("partner_id.name")[0]
                if float_compare(offer["price"], max_offer, precision_rounding=0.01) <= 0:
                    raise UserError(_(f"The new offer must be higher than the maximum offer of {max_offer:.2f} from {max_offer_partner_name}"))
        return super().create(vals_list)

    def action_accept(self):
        if "accepted" in self.property_id.offer_ids.mapped("state"):
            raise UserError(_("An offer has already been accepted."))
        self.write({ "state": "accepted" })
        for property in self.mapped("property_id"):
            property.write({
                "state": "offer_accepted",
                "selling_price": self.price,
                "buyer_id": self.partner_id.id,
            })
        return True

    def action_refuse(self):
        return self.write({ "state": "refused" })
