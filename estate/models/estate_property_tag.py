# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _explanation = "Represents a property tag"
    _order = "sequence"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=10)
