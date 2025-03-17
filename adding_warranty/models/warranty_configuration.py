# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class WarrantyConfiguration(models.Model):
    _name = "warranty.configuration"
    _description = "Shows warranty for all the products"

    name = fields.Char(string="Name", required=True)
    period = fields.Integer(string="Period", default="1", required=True)
    period_type = fields.Selection(
        [
            ("week", "Week"),
            ("month", "Month"),
            ("quarter", "Quarter"),
            ("year", "Year"),
        ],
        string="Period Type",
        required=True,
        default="year",
    )
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        required=True,
        domain=[("type", "=", "service")]
    )
    percentage = fields.Float(
        string="Percentage %",
        help="Price of warranty is Percentage of product price",
        required=True
    )
