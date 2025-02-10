from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"

    _sql_constraints=[
        (
            'unique_property_type', 'UNIQUE(name)', 'Property with this type already exists'
        )
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence=fields.Integer(string="Sequence")
    

