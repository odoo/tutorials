from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "My Estate Property Tag"

    name = fields.Char(required = True)
