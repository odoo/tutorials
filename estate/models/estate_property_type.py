from odoo import models, fields

class EstateType(models.Model):
    _name = "estate.property.type"

    name = fields.Char("Name")
    