from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property, such as home, apartment, row house"

    name = fields.Char(string="Property Type", required=True)

