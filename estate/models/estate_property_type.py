from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "test description 2"
    name = fields.Char(required=True)

