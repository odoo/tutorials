from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'The property Type'

    name = fields.Char(required=True)
    _sql_constraints = [
            ('type_name_unique', 'UNIQUE(name)', "The property type name must be unique.")
        ]