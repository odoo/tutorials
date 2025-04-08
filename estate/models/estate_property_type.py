from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Types'
    _sql_constraints = [
        (
            'estate_property_type_name_unique',
            'UNIQUE(name)',
            'The property types must be unique.',
        )
    ]

    name = fields.Char('Type', required=True)
