from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer on a Real Estate Property"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )

    validity = fields.Integer("Validity (in days)", default=7)

    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    partner_id = fields.Many2one("res.partner", string="Made by", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _check_price = models.Constraint("CHECK(price > 0)", "Offered price must be greater than zero")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            offer_date = record.create_date
            if not offer_date:
                offer_date = datetime.now()

            record.date_deadline = offer_date.date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            offer_date = record.create_date
            if not offer_date:
                offer_date = datetime.now()
            record.validity = (record.date_deadline - offer_date.date()).days

    def action_accept_offer(self):
        for record in self:
            linked_property = record.property_id
            states = linked_property.offer_ids.mapped("status")

            if "accepted" in states:
                raise UserError(_("An offer was already accepted"))

            if "cancelled" in states:
                raise UserError(_("Can't accept offers on cancelled auctions"))

            record.status = "accepted"
            linked_property.selling_price = record.price
            linked_property.buyer_id = record.partner_id
            linked_property.state = "offer_accepted"

        return True

    @api.model
    def create(self, vals):
        for offer in vals:
            linked_property = self.env["estate.property"].browse(offer["property_id"])
            if float_compare(offer["price"], linked_property.best_price, 2) < 0:
                raise UserError(_("Cannot lowball an existing offer"))

            if linked_property.state == "new":
                linked_property.state = "offer_received"

        return super().create(vals)

    def action_reject_offer(self):
        self.status = "refused"

        return True
