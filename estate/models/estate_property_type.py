# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)',
         'Property type name must be unique.')
    ]
    name = fields.Char(string="Property Type", required=True)
    sequence = fields.Integer(default=1)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
