# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details. 

from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = 'Real Estate Property Type'

    name = fields.Char("Property Type", required=True)
