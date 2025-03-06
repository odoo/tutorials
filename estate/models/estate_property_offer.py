from odoo import api, fields, models
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(string="Offer Price", required=True, default=0.0)
    validity = fields.Integer(string="Validity (days)", default=7)
    validity_date = fields.Date(string="Validity Date", compute="_compute_validity_date", inverse="_inverse_validity_date", store=True)

    @api.depends("create_date", "validity")
    def _compute_validity_date(self):
        for record in self:
            record.validity_date = record.create_date + timedelta(days=record.validity) if record.create_date else False

    def _inverse_validity_date(self):
        for record in self:
            if record.validity_date and record.create_date:
                record.validity = (record.validity_date - record.create_date.date()).days
                
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="Status", copy=False)
    
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
