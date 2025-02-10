from datetime import timedelta
from odoo import fields, models,api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        copy = False,
        selection=[
            ("offer_accepted", "Accepted"),
            ("refused","Refused")
        ])
    partner_id = fields.Many2one('res.partner', string='Partner', index=True, required = True)
    property_id = fields.Many2one("estate.property", required = True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends("create_date","validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date + timedelta(days=record.validity)) if record.create_date else False

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for record in self:
            accepted_offer = record.property_id.offer_ids.filtered(lambda offer: offer.status == "offer_accepted")
            if accepted_offer:
                raise UserError("An offer has already been accepted for this property.")
            record.status = "offer_accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.status = "offer_accepted"

    def action_reject(self):
        for record in self:
            record.status = "refused"
