from datetime import timedelta
from odoo import api,fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real estate system - Property Offer"
    
    price = fields.Float(string="Offer Price")
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity (days)",default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for offer in self:
            date=offer.create_date or fields.Date.today()
            offer.date_deadline=date+timedelta(days=offer.validity)
    
    def _inverse_date_deadline(self): 
        for record in self: 
            start = record.create_date.date() if record.create_date else fields.Date.today() 
            record.validity = (record.date_deadline - start).days  