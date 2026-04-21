from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tags (f.e. cozy)"
    _order = "name"

    name = fields.Char("Name", required=True)
    color = fields.Integer()

    _check_unique = models.Constraint(
        "UNIQUE(name)"
    )
