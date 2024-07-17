from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _sql_constraints = [
        ('type_unique', 'UNIQUE (name)', 'Type must be unique')
    ]
    
    name = fields.Char(required=True)
