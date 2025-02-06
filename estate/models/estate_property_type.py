from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char("Property Type", required=True, help="Property Type")
    property_id = fields.One2many("estate.property", "name")
    