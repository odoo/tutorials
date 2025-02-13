# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"
    _order = "name"
    _sql_constraints = [
        ('check_property_tag', 'UNIQUE(name)', 'Property Tag Must be Unique')]

    name = fields.Char(string="Tag", required=True)
    color = fields.Integer(string="Color")
