from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property Type"
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string="Properties"
    )

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'A property type with this name already exists.',
    )
