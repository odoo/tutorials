# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ProductKitWizardLine(models.TransientModel):
    _name = "productkit.line"
    _description = "Product kit wizard line"

    kit_product_line_id = fields.Many2one(comodel_name="productkit")
    product_id = fields.Many2one(comodel_name="product.product")
    kit_product_name = fields.Char(string="Product Name")
    kit_product_qty = fields.Integer(string="Quantity")
    kit_product_price = fields.Float(string="Price")

