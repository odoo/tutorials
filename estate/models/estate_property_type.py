from odoo import fields, models

class PropertyType(models.Model):

    _name = "estate_property_type"
    _description = "The type of the real estate property i.e. house, apartment, etc"
    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The name of the property type must be unique'),
    ]
    _order = 'name'
    property_ids = fields.One2many('estate_property', 'property_type_id')
    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help='Used for ordering property types. Lower is better')
