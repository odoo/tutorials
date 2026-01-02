from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.tag"
    _description = "Test-tag"

    name= fields.Char(string="Name")
