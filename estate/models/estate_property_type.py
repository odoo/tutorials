from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type'

    name = fields.Char('Title', required=True, translate=True)

    _type_name_uniq = (models.Constraint("""UNIQUE (name)""",
             "The type name must be unique."))
