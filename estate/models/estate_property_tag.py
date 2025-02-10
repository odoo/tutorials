# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    _sql_constraints = [
        ('unique_property_tag_name', 'UNIQUE(name)',
         'Property tag name must be unique.')
    ]
    name = fields.Char(string="Tag Name", required=True)
