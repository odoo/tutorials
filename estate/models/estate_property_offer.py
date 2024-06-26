from dateutil.relativedelta import relativedelta
from odoo import models, fields, tools, api

class PropertyOffer(models.Model):    
    # Model properties
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
    
    # Model fields
    price = fields.Float()
    status = fields.Selection(selection=[('accepted', "Accepted"), ('refused', "Refused")], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    
    
    # Calculate
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse="_inverse_date_deadline")
    
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity) 

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days
            