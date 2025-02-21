# Part of Odoo. See LICENSE file for full copyright and licensing details. 

from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property Tag"
    _order = 'name asc'
    _sql_constraints = [
        ('unique_tag_name', "UNIQUE(name)", "The property tag name must be unique."),
    ]

    name = fields.Char('Tag Name', required=True)
    color = fields.Integer(string="Color")
