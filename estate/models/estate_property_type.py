from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"

    name = fields.Char(string='Name',
                       required=True,
                       help='This is the estate property type.')

    _sql_constraints = (
        ('unique_name', 'UNIQUE(name)',
         'Type name should be unique'),
    )

    property_ids = fields.One2many("estate.property", "property_type_id")

    _order = "name"
