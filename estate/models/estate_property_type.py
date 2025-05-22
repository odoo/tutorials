from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "ch7 exercise tutorial"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)',
         'Each property type should have a unique name.')
    ]