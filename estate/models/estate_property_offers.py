from odoo import fields, models,api 
from datetime import timedelta, datetime

class EstatePropertyOffers(models.Model):

    _name = "estate.property.offers"
    _description = "Estate Property Offers Model"
    
    price = fields.Float(string='Offer Price')
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
       )
    partner_id = fields.Many2one('res.partner', required=True) 
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute = "_compute_date_deadline", inverse="_inverse_date_deadline", store="True")

    # Functions
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(record.validity)
            else:
                record.date_deadline = datetime.today() + timedelta(7)
    
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 7
    
