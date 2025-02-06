# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models,fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "tags attached to property"
    
    name = fields.Char(string="Property Tag" , required=True)
