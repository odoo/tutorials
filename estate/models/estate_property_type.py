from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "My Estate Property Type"

    name = fields.Char(required = True)
