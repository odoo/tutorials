from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of Property"

    name = fields.Char(required=True)
