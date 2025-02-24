# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields
from odoo import models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Estate Property Tag"
    _order = 'name'
    _sql_constraints = [
        ('property_tag_unique', "UNIQUE(name)",
        "Tag with same name already exists"),
    ]

    name = fields.Char(required=True)
    color = fields.Integer()
