# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class WarrantyConfig(models.Model):
    _name = "warranty.config"
    _description = "Warranty Configuration"

    name = fields.Char(string="Name")
    product = fields.Many2one(comodel_name="product.product", string="Product")
    percentage = fields.Float(string="Percentage")
    period = fields.Float(string="Period (in Years)", default=1)
