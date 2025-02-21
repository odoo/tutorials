from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "test description 3"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer("Color", default=0xFFFFFF)

    _sql_constraints = [
        ("unique_property_tag", "UNIQUE(name)", "Property tag should be unique")
    ]
