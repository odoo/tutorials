from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Type name must be unique!')
    ]

    name = fields.Char("Property Type", required=True, help="Property Type")
    property_ids = fields.One2many("estate.property", "property_type_id")
    