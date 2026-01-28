import random
from odoo import models, fields


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    # constraints
    _unique_tag = models.Constraint(
        'UNIQUE(name)',
        'Tag name should be unique'
    )

    name = fields.Char(string="Name", required=True)
    color = fields.Integer('Color Index', default=lambda self: random.randint(1, 11))
