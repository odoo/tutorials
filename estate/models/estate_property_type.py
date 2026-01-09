from typing import Sequence
from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property types"
    _order = 'name'

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type")
    sequence = fields.Integer()
    _uniq_tag_name = models.Constraint(
        "unique(name)",
        "A Property Type already exist, Propert type should be unique.",
    )
