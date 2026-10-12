from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "this is used to define the types"

    name = fields.Char(required=True, string="Type")
    _check_name = models.Constraint(
        'unique(name)',
        'The name of the property type must be unique'
    )
