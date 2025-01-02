from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float()
    property_id = fields.Many2one('estate.property',required=True)
    partner_id = fields.Many2one('res.partner', required=True)
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
            ('pending', 'Pending')
        ],
        default='pending',  copy=False
    )