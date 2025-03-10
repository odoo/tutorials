from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(required=True)
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'A property type name must be unique')
    ]