from odoo import fields, models

class PropertyOffer(models.Model):
    _name = "property.offer"
    _description = "Property Offer"

    name = fields.Char(required=True)
    property_id = fields.Many2one('estate.property', string='Property')
    price = fields.Float(required=True)
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string='Partner')
