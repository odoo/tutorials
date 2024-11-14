from odoo import fields, models, api
from datetime import timedelta, date
class EstatePropertyOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    
    price = fields.Float()
    status = fields.Selection([('ACCEPTED', 'Accepted'),('REFUSED','Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    