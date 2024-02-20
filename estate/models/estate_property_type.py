from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True, string="Type")

    _sql_constraints = [
        ('property_type_name_unique', 'UNIQUE (name)', 'The name must be unique.'),
    ]
