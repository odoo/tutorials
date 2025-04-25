from datetime import date

from odoo import fields, models, api
from odoo.tools import date_utils
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers made on a listing"
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
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline",
    )
    sold = fields.Boolean(default="false")

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
            if offer.sold:
                raise UserError("An offer has already been accepted!")
                return False
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.sold = False
        return True

    def action_offer_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True
