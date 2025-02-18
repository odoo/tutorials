# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"
    
    name = fields.Char('Name', required=True, translate=True)
    property_ids = fields.Many2many('estate.property', 'property_tag_ids')