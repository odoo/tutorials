# -*- coding: utf-8 -*-

from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate property tag"

    name = fields.Char("Tag", required=True)
