# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Real Estate Property Tag"
    _order = 'name'

    _check_unique_name = models.Constraint('UNIQUE(name)', "The tag name must be unique.")

    name = fields.Char(required=True, string="Name")
    color = fields.Integer(string="Color")
