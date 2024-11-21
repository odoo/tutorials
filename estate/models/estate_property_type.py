from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property Type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_property_type_name_check', 'UNIQUE(name)',
         'Type name should be unique.'),
    ]
