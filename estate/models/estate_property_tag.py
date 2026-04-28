from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()
    _check_name_unique = models.Constraint(
        "UNIQUE(name)", "A property tag name must be unique."
    )
