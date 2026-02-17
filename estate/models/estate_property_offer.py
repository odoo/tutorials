from odoo import models, fields, api
from odoo.tools.date_utils import relativedelta

PROPERTY_OFFER_STATE = [("accepted", "Accepted"), ("refused", "Refused")]


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(selection=PROPERTY_OFFER_STATE, copy=False)

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept_offer(self):
        for record in self:
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            for offer in record.property_id.offer_ids:
                if offer != record:
                    offer.status = "refused"
        return True
    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"
        return True
