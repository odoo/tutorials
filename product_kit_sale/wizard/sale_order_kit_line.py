# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleOrderKitLine(models.TransientModel):
    _name = "sale.order.kit.line"
    _description = "Sale Order Kit product"

    wizard_id = fields.Many2one(comodel_name="sale.order.kit", required=True, ondelete="cascade")
    product_id = fields.Many2one(comodel_name="product.product", required=True, ondelete="cascade")
    quantity = fields.Float(string="Quantity")
    price_unit = fields.Float(string="Price")
