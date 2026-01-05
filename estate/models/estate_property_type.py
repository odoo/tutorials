from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Defines types of property"

    name = fields.Char(string="Name", required=True)
