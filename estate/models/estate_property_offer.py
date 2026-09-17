from odoo import fields, models


class Offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer for a property of Estate'

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        index=True,
        required=True
    )
    property_id = fields.Many2one('estate.property', required=True)
