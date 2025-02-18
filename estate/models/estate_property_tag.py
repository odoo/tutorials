from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"

    name = fields.Char('Name')
