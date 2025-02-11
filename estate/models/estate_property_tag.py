from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char()
    color = fields.Integer("Color", default=1)

    _sql_constraints = [
        ("unique_property_tag", "UNIQUE(name)", "Property tag should be unique")
    ]

