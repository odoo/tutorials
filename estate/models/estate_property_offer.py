from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "estate property offers"

    # simple fields
    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', "Accepted"),
                   ('refused', "Refused"),
                   ],
        copy=False,
        )
    # relational fields
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    