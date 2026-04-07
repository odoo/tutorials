from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property_type"
    name = fields.Char(string="Property Type", required=True)
