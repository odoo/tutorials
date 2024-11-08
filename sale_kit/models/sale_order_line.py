from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    parent_sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', ondelete='cascade')
    subproduct_price = fields.Float()
    is_kit = fields.Boolean(related='product_id.is_kit')
