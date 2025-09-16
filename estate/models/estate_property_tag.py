from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Test description for estate.property.tag model"

    name               = fields.Char(required=True)