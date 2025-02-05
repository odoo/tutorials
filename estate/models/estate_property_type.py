from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate properties type"

    name = fields.Char('Type', required=True)
