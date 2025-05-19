# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag for real estate properties"
    _order = "name"

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color')

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The name must be unique.'),
    ]
