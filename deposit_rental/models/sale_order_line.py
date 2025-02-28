# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_deposit_line = fields.Boolean("Is Deposit Line", default=False)
    linked_product_id = fields.Many2one('product.product', "Linked Rental Product")
