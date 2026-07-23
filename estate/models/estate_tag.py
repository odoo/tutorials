from odoo import models, fields

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Tag"

    name = fields.Char(string="Tag")
