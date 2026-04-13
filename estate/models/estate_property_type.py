from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property_type"
    _description = "Defines property type"
    name = fields.Char(string="Property Type", required=True)
    _name_unique = models.UniqueIndex("(name)", "name must be unique")
