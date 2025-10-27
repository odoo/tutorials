from odoo import models
from odoo.fields import Char, Integer


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate tags"
    _order = "name"

    name = Char(required=True)
    color = Integer()

    _check_name_is_unique = models.Constraint(
        'unique(name)',
        'The tag name should be unique',
    )
