# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Estate property Tag"
    
    name = fields.Char(string="Name", required=True)
    color = fields.Integer()
    _sql_constraints = [
        ('check_tag_name', "UNIQUE(name)", "Tag name must be unique. Please choose a different name.")
    ]
