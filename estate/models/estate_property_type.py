from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property type"
    name = fields.Char("Property Type", required=True)
