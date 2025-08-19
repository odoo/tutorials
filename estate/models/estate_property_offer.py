from odoo import models, fields

class EstateOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer Model"

    price = fields.Float()
    status = fields.Selection([
        ('Accepted', 'Accepted'),
        ('Refused', 'Refused')
    ], copy=False)
    partner_id= fields.Many2one('res.partner', required=True)
    property_id= fields.Many2one('estate.property', required=True)