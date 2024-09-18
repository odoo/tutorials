from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('property_type_name_unique', 'UNIQUE(name)', 'Property type name must be unique')
    ]