# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Estate property tag"

    _name_uniq = models.Constraint(
        'UNIQUE(name)',
        'The tag name must be unique.',
    )

    name = fields.Char('Tag name', required=True)
