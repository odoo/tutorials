# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean(string='Is Kit?', default=False)
    sub_product_ids = fields.Many2many(comodel_name="product.product", string="Sub Products", store=True)
