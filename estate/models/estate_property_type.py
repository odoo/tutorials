from odoo import models,fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Model for property types"
    _order = "name"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)', 
         'Property type name must be unique.')
    ]
