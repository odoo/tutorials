# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

from random import randint


class EstateTag(models.Model):
    _name = "estate.tag"
    _description = "Estate Tag"
    _order = "name"

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char("Name", required=True, translate=True)
    color = fields.Integer(
        string='Color Index', default=lambda self: self._default_color(),
        help='Tag color. No color means no display in kanban or front-end, to distinguish internal tags from public categorization tags.')

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The tag name has to be unique',
    )
