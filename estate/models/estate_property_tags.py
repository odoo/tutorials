import random

from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = 'estate.property.tags'
    _description = "Estate Property Tags"

    name = fields.Char("Property Tags", required=True)
    color = fields.Integer('Color Index', default=lambda self: random.randint(1, 11))

    # SQL CONSTRAINT
    _property_tag_uniq = models.Constraint(
        'unique(name)', "Property Tags already exist in database"
    )
