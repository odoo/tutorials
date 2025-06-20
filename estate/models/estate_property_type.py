from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    # misc
    name = fields.Char(string='Type', required=True)