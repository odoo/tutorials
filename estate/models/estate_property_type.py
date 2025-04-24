from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Property type name must be unique')
    ]
    name = fields.Char(required=True)
