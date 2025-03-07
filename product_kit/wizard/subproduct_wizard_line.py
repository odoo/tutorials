# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class SubproductWizardLine(models.TransientModel):
    _name = 'subproduct.line'
    _description = 'Sub-product Wizard Line'

    kit_product_line_id = fields.Many2one('subproduct')
    product_id = fields.Many2one('product.product')
    kit_product_name = fields.Char(string="Product Name")
    kit_product_qty = fields.Integer(string="Quantity")
    kit_product_price = fields.Float(string="Unit Price")
