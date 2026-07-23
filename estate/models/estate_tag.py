from odoo import models, fields

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Tag"

    name = fields.Char(string="Tag")

    _name_idx = models.UniqueIndex('(name)', 'Another record already exists with the same name!')
