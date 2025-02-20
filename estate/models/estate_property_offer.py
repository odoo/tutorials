from odoo import models, fields, api
from datetime import datetime, timedelta

class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'my estate property offer'

    price = fields.Float(required=True)
    partner_id = fields.Many2one('res.partner', string="Partner")
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
            ('pending', 'Pending'),
        ],
        default='pending',
        copy=False,
    )