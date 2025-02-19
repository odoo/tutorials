from odoo import models, fields


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _sql_constraints = [
        ("unique_tag_name", "UNIQUE(name)", "The name of a tag must not already exist"),
    ]

    name = fields.Char(required=True)
