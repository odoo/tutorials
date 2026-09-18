from odoo import fields, models


class EstatePropertyTypeModel(models.Model):
    _name = "estate_property_type"
    _description = "The type of an estate"

    name = fields.Char(required=True)

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'A property tag name must be unique',
    )
