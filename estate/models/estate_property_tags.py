from odoo import models, fields


class Estatepropertytags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property Tags"

    name = fields.Char(required=True)

    _sql_constraints = [
        (
            "check_property_tagname",
            "UNIQUE(name)",
            "Property Tag name must be unique",
        )
    ]
