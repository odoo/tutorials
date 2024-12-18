from odoo import fields, models


class RealEstatePropertyType(models.Model):
    _name = 'real.estate.property.type'
    _description = "Real Estate Property Type"
    _sql_constraints = [
        ('unique_name', 'unique(name)', "A property type name must be unique.")
    ]

    name = fields.Char(string="Name", required=True)
