from odoo import fields, models


class Estatepropertytags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property Tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer("Tag Colour")

    _sql_constraints = [
        (
            "check_property_tagname",
            "UNIQUE(name)",
            "Property Tag name must be unique",
        )
    ]
