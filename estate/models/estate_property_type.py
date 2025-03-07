from odoo import fields, models


class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Help to set type for property"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string=" ")

    _sql_constraints = [("unique_type_name", "UNIQUE(name)", "Type must be Unique")]
