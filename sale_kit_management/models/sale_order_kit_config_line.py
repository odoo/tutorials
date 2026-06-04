from odoo import fields, models


class SaleOrderKitConfigLine(models.Model):
    _name = 'sale.order.kit.config.line'
    _description = "Kit Configuration Line"

    sale_order_line_id = fields.Many2one('sale.order.line', string="Kit Parent Line", ondelete='cascade', required=True, index=True)
    product_id = fields.Many2one('product.product', string="Product", required=True)
    kit_unit_qty = fields.Float(string="Kit Unit Qty", default=1.0)
    price_unit = fields.Float(string="Unit Price")
