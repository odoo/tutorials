# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    has_kit = fields.Boolean(string="Is Kit")
    kit_products = fields.Many2many(
        comodel_name="product.product", string="Sub Products"
    )

