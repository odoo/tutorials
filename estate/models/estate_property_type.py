from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    _order = "sequence, name asc" 

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer("Sequence", default=10)
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The property type name must be unique.')
    ]
