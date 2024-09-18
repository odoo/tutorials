from odoo import api, fields, models
from datetime import date, timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Define an offer for a given property'

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
            ]
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", string="Deadline")
    
    
    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = date.today()
            record.date_deadline = record.create_date + timedelta(days=record.validity)
            
    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
    