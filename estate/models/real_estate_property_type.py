from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"

    name = fields.Char(string="Name")

    _name_unique = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique'
    )
