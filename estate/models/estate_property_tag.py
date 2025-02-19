# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields,models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property Tags"
    _order = "name desc"

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="Color")
