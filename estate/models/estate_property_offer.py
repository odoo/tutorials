from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer description"

    price = fields.Float(string="Price")
    property_offer_ids = fields.Integer(string="Offer")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
    )
    validity = fields.Integer(string="Validity(days)", default=7)
    date_deadline = fields.Date(
        compute="_compute_sum_date",
        inverse="_compute_validity",
        string="Deadline",
    )

    def action_btn_accepted(self):
        for record in self:
            if record.status == "refused":
                raise UserError(msg="Sorry offer sold out.")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_btn_refused(self):
        for record in self:
            if record.status == "accepted":
                raise UserError(msg="Offer is already refudsed")
            record.status = "refused"
            record.property_id.selling_price = "0"
            record.property_id.buyer_id = ""
        return True

    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends("validity")
    def _compute_sum_date(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _compute_validity(self):
        for record in self:
            fields.Date.today() == record.date_deadline - timedelta(
                days=record.validity,
            )
