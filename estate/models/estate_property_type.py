from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True, string="Name")
    
    _sql_constraints = [
        ('check_expected_price', 'UNIQUE (name)', 'A property type name must be unique'),
    ]