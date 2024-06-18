from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of real estate property"

    name = fields.Char(required=True, string="Type")

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)', 'Property types must be unique')
    ]