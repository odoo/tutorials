from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"
    
    _sql_constraints=[
        (
            'unique_property_type', 'UNIQUE(name)', 'Property with this type already exists'
        )
    ]
    
    name = fields.Char(string="Name", required=True, help="Property Type")
    active = fields.Boolean(default=True)
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="property_type_id")
    sequence=fields.Integer(string="Sequence")
