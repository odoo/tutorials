from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"

    name = fields.Char(string="Name")

    _name_unique = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique'
    )
