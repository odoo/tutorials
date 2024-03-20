# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('name_unique', 'unique (name)', "Tag name already exists!"),
    ]
