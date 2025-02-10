from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types for Real Estate App"

    name = fields.Char(required=True)
