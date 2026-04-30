from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _check_name = models.Constraint(
        'UNIQUE(name)',
        'A property tag name must be unique',
    )
