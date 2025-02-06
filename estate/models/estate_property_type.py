from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Contains all property type"

    name = fields.Char(string="Property Type", required=True)
