from random import randint

from odoo import fields, models


class EstatePropertyTag(models.Model):
    """A label characterizing properties (cozy, renovated...)."""

    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    def _default_color(self):
        """Give each new tag a random color (0 means no color in Odoo)."""
        return randint(1, 11)

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color", default=_default_color)

    _name_uniq = models.Constraint(
        'UNIQUE(name)',
        'The property tag name must be unique.',
    )
