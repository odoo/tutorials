# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Real Estate Property Tag"
    _order = 'name asc'
    _sql_constraints = [
        ('check_unique_tag_type', 'UNIQUE(name)',
         'Property tag is already exists')
    ]

    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer(string="Color", default=5)
