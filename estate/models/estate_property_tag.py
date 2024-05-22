# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Real Estate property tags"
    _order = 'name'
    _sql_constraints = [('name_unique', 'UNIQUE(name)', "Name must be unique.")]

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")
