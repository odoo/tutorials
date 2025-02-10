# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags attached to the property"
    _sql_constraints = [
        ("unique_tag_name", "UNIQUE(name)", "Property tag name must be unique."),
    ]
    _order = "name"

    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer(string="Color")
