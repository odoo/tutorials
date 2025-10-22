from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = 'name asc'

    _name_unique = models.Constraint(
        'unique (name)',
        "A property tag name must be unique.",
    )

    name = fields.Char(required=True)
    color = fields.Integer()
