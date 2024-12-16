# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Used to describe the type of the property i.e House, Apartment, etc."

    name = fields.Char(string="Name", required=True)