# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class WarrantyConfiguration(models.Model):
    _name = "warranty.configuration"
    _description = "Shows warranty for all the products"

    name = fields.Char(string="Name", required=True)
    period = fields.Integer(string="Period(in year)", default="1")
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        required=True,
        domain=[("type", "=", "service"), ("name", "ilike", "warranty")]
    )
    percentage = fields.Float(
        string="Percentage %",
        help="Price of warranty is Percentage of product price",
        required=True
    )
