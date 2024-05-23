from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of real estate property"

    name = fields.Char(required=True)
    