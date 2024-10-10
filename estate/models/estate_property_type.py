from odoo import fields, models  # type: ignore

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Ayve"

    name = fields.Char(required=True)
    property_id = fields.One2many('estate.property',"property_type_id", string="Property")
    