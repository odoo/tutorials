from datetime import timedelta
from odoo import fields, models,api

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
