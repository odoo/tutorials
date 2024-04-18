from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("unique_tag_name", 'unique(name)', 'A property tag name and property type name must be unique')
    ]
