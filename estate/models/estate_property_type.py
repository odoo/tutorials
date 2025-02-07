from odoo import fields, models

class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property', 'property_type',
        string='Properties',
    )
    sequence = fields.Integer('Sequence')

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)',
         'A property type must be unique')
    ]