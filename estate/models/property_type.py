from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property types"

    name = fields.Char(required=True)
