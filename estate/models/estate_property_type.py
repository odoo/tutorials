from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', "The property type name must be unique."),
    ]
    