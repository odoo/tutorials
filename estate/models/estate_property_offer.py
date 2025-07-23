from odoo import models, fields, api
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    
    price = fields.Float()
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                # Fallback for when create_date is not set yet
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            elif record.date_deadline:
                # Fallback for when create_date is not set yet
                record.validity = (record.date_deadline - fields.Date.today()).days
