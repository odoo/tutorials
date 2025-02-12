# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description = "Estate property Tag"
    _order = "name asc"
    
    name=fields.Char("Name", required=True)
    color=fields.Integer()
    
    _sql_constraints=[
        ("check_tag_name", "UNIQUE(name)", "Please add differant tag name")
    ]
