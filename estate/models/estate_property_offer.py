from odoo import models, fields

class PropertyOffer(models.Model):

    _name = "estate_property_offer"
    _description = "An offer to buy a real estate property"
    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('Accepted', 'Accepted'),
            ('Refused', 'Refused'),
        ],
        copy = False
    )
    partner_id = fields.Many2one('res.partner', string = "Partner", required = True)
    property_id = fields.Many2one('estate_property', required = True)