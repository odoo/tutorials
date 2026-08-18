from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Properties Type"

    name = fields.Char("Type", required=True)
