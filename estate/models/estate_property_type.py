from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)', 'Property Type name must be unique.')
    ]
