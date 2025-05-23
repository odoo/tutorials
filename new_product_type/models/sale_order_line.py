# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    product_is_kit = fields.Boolean(related='product_template_id.is_kit')
    parent_sale_order_line_id = fields.Many2one(comodel_name='sale.order.line')
    child_sale_order_line_ids = fields.One2many(comodel_name='sale.order.line', inverse_name='parent_sale_order_line_id')
    actual_price_sub_product = fields.Float(string="Price")
