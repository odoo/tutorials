from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of properties"

    name = fields.Char(required=True)
