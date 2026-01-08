from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"

    name = fields.Char(string="Name")

    _tag_name_unique = models.Constraint(
        'UNIQUE(name)',
        'The property tag name must be unique.',
    )
