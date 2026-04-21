from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name asc"

    name = fields.Char(required=True)

    color = fields.Integer()

    _check_unique_property_tags = models.Constraint(
        'unique(name)'
    )
