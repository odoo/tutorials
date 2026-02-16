from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"

    name = fields.Char(string="Property Type", required=True)
    property_type_id = fields.Integer()
