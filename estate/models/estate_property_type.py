from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    
    # Basic Fields
    name = fields.Char(required=True)
    
    # SQL Constraints
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Type name must be unique.'),
    ]
