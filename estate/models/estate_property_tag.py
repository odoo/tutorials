# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Contains all property tags"
    _order = "name"

    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer(string="Tag Color")

    _sql_constraints = [('name_uniq', 'unique(name)', 'Property Tag already exists')]
