from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(default=1)

    _check_property_tag_name_unique = models.Constraint(
        'UNIQUE(name)',
        'The name of the property tag must be unique.'
    )
