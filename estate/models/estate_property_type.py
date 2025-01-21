# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyType(models.Model):
    
    _name = "estate.property.type"
    _description = "Estate property type"
    _order= "sequence asc, name asc" #to order the data in inc ordering of type
    
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.") #to enable manual order the property type in 
    name= fields.Char(string="Name", required=True)
    _sql_constraints= [
        ('unique_name_check', 'UNIQUE(name)', 'Given Property type already exist please choose unique property type')
    ]
    
    def get_all_property_offers_related(self):
        pass
