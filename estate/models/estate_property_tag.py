# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(string='Property Tag', required=True)

    _tag_name_uniq = models.Constraint(
        'unique(name)',
        "The property tag name must be unique",
    )
