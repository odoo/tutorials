from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of properties available in the estate module."


    name = fields.Char('Name', required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Property"
    )
