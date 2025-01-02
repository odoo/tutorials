# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyType(models.Model):
    
    _name = "estate.property.type"
    _description = "Estate property type"

    name= fields.Char(string="Name", required=True)
    _sql_constraints= [
        ('unique_name_check', 'UNIQUE(name)', 'Given Property type already exist please choose unique property type')
    ]
    