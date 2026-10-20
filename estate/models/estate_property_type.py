from odoo import fields, models


class PropertyTypes(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"

    name = fields.Char(string="Property Type", required=True)
