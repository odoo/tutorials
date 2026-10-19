from odoo import fields, models  # ty: ignore[unresolved-import]


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property for real estate"

    name = fields.Char(required=True)
