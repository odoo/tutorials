from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type module for Odoo 19 tutorials Hello World"

    name = fields.Char(required=True, string="Property Type Name")

    _check_unique_type_name = models.Constraint(
        'UNIQUE(name)',
        'The property type name must be unique.',
    )
