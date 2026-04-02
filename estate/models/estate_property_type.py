from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"

    name = fields.Char(string="Type", required=True)

    _unique_type_name = models.Constraint(
        'unique(name)',
        'The property type name must be unique.'
    )
