# -*- coding: utf-8 -*-

from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"

    name = fields.Char("Property Type", required=True)
