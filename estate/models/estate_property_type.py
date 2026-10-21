from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property for the estate module"

    name = fields.Char(required=True)

    _name_param_uniq = models.Constraint(
        'UNIQUE (name)',
        'A property selling price must be positive'
    )
