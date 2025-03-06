from odoo import models, fields # type: ignore

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Property Types")