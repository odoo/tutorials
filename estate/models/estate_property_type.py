from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"

    name = fields.Char(string="Property Type", required=True)
