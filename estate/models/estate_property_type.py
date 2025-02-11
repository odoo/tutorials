from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(string="Name", required=True)

    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)', 'The property type name must be unique.')
    ]
