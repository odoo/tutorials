from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "A real estate property type such as a house, apt..."

    name = fields.Char(string="Property Type", required=True)

    test_value = fields.Char(string="Test Value", required=True)

    sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Type name must be unique'),
    ]
