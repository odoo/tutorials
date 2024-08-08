from odoo import models, fields


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Estate property type"

    name = fields.Char(string='Name', required=True)
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string="property")

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'THE PROPERTY TYPE NAME MUST BE UNIQUE ! ...')
    ]
