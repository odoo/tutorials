from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ]
    )
    partner_id = fields.Many2one('res.partner', string='Buyer', required=True) 
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    

