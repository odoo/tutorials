# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class WarrantyConfiguration(models.Model):
    _name = "warranty.configuration"
    _description = "Shows warranty for all the products"

    name = fields.Char(string="Name", required=True)
    period = fields.Integer(string="Period(in year)", default="1")
    product_id = fields.Many2one("product.product", string="Product", required=True)
    percentage = fields.Float(string="Percentage %", help="Price of warranty is Percentage of product price", required=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        product_ids = records.mapped('product_id')
        if product_ids:
            product_ids.write({'sale_ok': False, 'purchase_ok': False, 'type': 'service'})
        return records
