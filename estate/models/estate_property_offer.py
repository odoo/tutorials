from odoo import models, fields, api

class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "this is defind the offer of properties"

    price = fields.Float("offer_price")
    status = fields.Selection(
        [("Accepted", "accepted"), ("Refused", "refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate_property", required=True)

    validity = fields.Integer("Offer Validity", default=7)
    date_deadline = fields.Date(
        "Deadline", compute="_compute_deadline", inverse="_compute_validity"
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                record.create_date or fields.Date.today(), days=record.validity
            )

    def _compute_validity(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
