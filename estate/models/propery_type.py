# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PropertyType(models.Model):
    _name = "property_type"
    _description = "Property Types"
    name = fields.Char(required=True)
