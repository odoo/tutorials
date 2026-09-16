from odoo import models, fields


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Property Offer"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ]
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', required=True)
