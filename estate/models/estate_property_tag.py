import random

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Type"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(default=lambda: random.randint(1, 10))

    _sql_constraints = [("check_property_tag_name", "unique(name)", "Two property tags cannot have the same name.")]
