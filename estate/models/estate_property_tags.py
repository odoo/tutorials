from odoo import models, fields
import random


class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property Tags"
    _order = "name"
    name = fields.Char(required=True)
    color = fields.Integer(
        string="Color Index", default=lambda self: self._default_color()
    )
    _sql_constraints = [
        ("name_uniq", "unique(name)", "Tags must be unique"),
    ]

    def _default_color(self):
        return random.randint(1, 11)
