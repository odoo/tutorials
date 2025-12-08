from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Defines the type of Real Estate Property"

    name = fields.Char(required=True)
