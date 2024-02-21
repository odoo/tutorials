from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"

    name = fields.Char(string='Name',
                       required=True,
                       help='This is the estate property type.')
