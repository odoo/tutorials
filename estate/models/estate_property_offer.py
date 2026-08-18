from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float('Price', required=True)
    property_id = fields.Many2one('estate.property', 'property_id', required=True)
    partner_id = fields.Many2one('res.partner', required=True)
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ]
    )

