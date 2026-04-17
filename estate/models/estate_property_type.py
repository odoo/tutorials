from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Types'
    _rec_name = 'type'

    colour = fields.Selection(
        [
            ('red', 'Red'),
            ('green', 'Green'),
            ('yellow', 'Yellow')
        ]
    )
    type = fields.Char(required=True)
