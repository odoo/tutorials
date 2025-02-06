from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property Type"

    name = fields.Char(string="Type", required=True)

    property_ids=fields.One2many('estate.property','property_type_id')

    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)', 'Property type name must be unique!')
    ]
