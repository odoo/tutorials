from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Test description for estate.property.type model"

    name               = fields.Char(required=True)