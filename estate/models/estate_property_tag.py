# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models,fields 


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(string="Tag",required=True)
    property_ids = fields.Many2many("estate.property", string="Properties")



