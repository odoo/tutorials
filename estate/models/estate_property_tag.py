# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name asc" # apply order on whole model, default_order attribute in listview for xml apply order on particular view.

    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('check_unique_tag_type', 'UNIQUE(name)',
         'Property tag is already exists')
    ]
