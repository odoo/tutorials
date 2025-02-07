from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type like House, Apartment, Penthouse"

    name = fields.Char(required=True)
