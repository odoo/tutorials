from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property Types"
    _order = "name"
    
    _sql_constraints = [
        ("unique_property_type_name", "UNIQUE(name)", "Type Name must be Unique")
    ]

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
