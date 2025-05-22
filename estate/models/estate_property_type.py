from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Type of a property'
    _sql_constraints = [
        ('check_unicity', 'UNIQUE (name)', 'A property type with the same name already exists'),
    ]

    name = fields.Char('Property Type', required=True)
