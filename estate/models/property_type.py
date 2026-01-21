from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(string="Property Type", required=True)
