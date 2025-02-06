from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name asc"

    name = fields.Char(string="Property Type", required=True)