from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"

    name = fields.Char(required=True)

    _check_unique_tag = models.Constraint(
        'UNIQUE(name)', "A property tag name must be unique!"
    )
