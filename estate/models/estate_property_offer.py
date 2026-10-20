from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer"

    property_id = fields.Many2one('estate.property', string='Property')

    price = fields.Float(string='Price', required=True)
    buyer_id = fields.Many2one('res.partner', string='Partner', index=True)
    state = fields.Selection(
        [('refused', 'Refused'),
         ('accepted', 'Accepted'),
         ('waiting', 'Waiting')],
        default='waiting'
    )
