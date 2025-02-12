from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"
    _order = "name"

    _sql_constraints = [
        ("unique_property_tag_name", "UNIQUE(name)", "Tag Name must be unique")
    ]

    name = fields.Char(string="Property Tag", required=True)
