from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "  Real Estate Property Type"

    name = fields.Char(string="Property Type", required=True)
    # property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")

    _sql_constraints = [
        ("unique_type_name", "UNIQUE(name)", "The property type name must be unique.")
    ]
