from random import randint

from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char("Name", required=True, translate=True)
    sequence = fields.Integer('Sequence', default=0)
    color = fields.Integer(
        string='Color Index', default=lambda self: self._default_color(),
        help='Tag color. No color means no display in kanban or front-end, to distinguish internal tags from public categorization tags.'
    )

    _name_uniq = models.Constraint(
        'unique(name)',
        'A property tag with the same name already exists.',
    )
