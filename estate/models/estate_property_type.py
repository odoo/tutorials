from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "ch7 exercise tutorial"

    name = fields.Char(required=True)
