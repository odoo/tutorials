from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.tag"
    _description = "Type of property tags"

    name = fields.Char(required=True)