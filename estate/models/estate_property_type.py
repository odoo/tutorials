# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Contains all property type"
    _order = "sequence, name"

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many(string="Properties", comodel_name="estate.property", inverse_name="property_type_id")
    sequence = fields.Integer(string="Sequence")

    _sql_constraints = [('name_uniq', 'unique(name)', 'Property Type already exists')]
