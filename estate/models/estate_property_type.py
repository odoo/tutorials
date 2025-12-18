from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(name="Name", required=True)
