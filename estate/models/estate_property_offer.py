from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):

    _name = 'estate.property.offer'
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.to_date(record.create_date) or fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = record.date_deadline - record.create_date

    def action_confirm(self):
        for record in self:
            if record.status == "refused":
                raise UserError("You can't accept an refused offer.")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id.id
            record.property_id.action_set_sold()
            for offer in record.property_id.offer_ids:
                if offer.status != "accepted":
                    offer.status = "refused"
        return True

    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("You can't refuse an accepted offer.")
            record.status = "refused"
        return True
