from odoo import fields, models

class PropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Estate property types"

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'A property type name must be unique.')
    ]

    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer()
