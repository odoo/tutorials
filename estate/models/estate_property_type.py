from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(string="Name", required=True)

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)', 'Property type must be unique'),
    ]
