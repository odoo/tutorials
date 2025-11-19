from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'All property types'
    _order = 'name asc'

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string="Properties",
    )
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types.")
