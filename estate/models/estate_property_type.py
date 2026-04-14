from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Types'
    _rec_name = 'type'

    type = fields.Char(required=True)
    colour = fields.Selection(
        [
            ('red', 'Red'),
            ('green', 'Green'),
            ('yellow', 'Yellow')
        ]
    )
