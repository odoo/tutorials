from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'An offer for a property'

    price = fields.Float(default=0.0)
    status = fields.Selection([
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], default='new', copy=False)

    partner_id = fields.Many2one('res.partner', string='Buyer')
    property_id = fields.Many2one('estate.property', string='Property')
