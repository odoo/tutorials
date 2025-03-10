from random import randint
from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.tags"
    _description = "Tags for Estate"
    _order = "name"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char("Tag", required=True)
    color = fields.Integer(string="Color", default=_get_default_color)

    _sql_constraints = [("unique_tag_name", "unique(name)", "Tag already exists.")]
