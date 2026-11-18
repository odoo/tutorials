from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type'

    name = fields.Char(required=True)
    """ property_type = fields.Selection(
        selection=[
            ('house', 'House'),
            ('apartment', 'Apartment'),
            ('penthouse', 'Penthouse'),
            ('castle', 'Castle')
        ]
    ) """
