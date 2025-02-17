# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Real Estate Property Types"
    
    name = fields.Char('Name', required=True, translate=True)
    property_ids = fields.Many2many('estate.property', 'property_tags_id')