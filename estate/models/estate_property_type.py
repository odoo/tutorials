from odoo import fields, models

class Property_Type(models.Model):
    _name = "estate.property.type"
    _description = "Property type"
    name = fields.Char(required=True)