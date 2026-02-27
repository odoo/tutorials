import random

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _order = "name"

    def _get_default_color(self):
        return random.randint(0, 10)

    name = fields.Char('Tag', required=True)
    color = fields.Integer(default=_get_default_color)

    _check_name = models.Constraint("UNIQUE(name)", "Tag name must be unique.")
