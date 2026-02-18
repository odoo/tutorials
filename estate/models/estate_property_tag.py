# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate properties tags"
    _order = "name"

    name = fields.Char('Property Tags', required=True)
    color = fields.Integer()

    _check_unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name of a property tag should be unique.',
    )
