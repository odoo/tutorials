from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_kit = fields.Boolean(related='product_template_id.is_kit')
    sale_order_line_id = fields.Many2one('sale.order.line', ondelete='cascade')
    previously_set_price = fields.Float()
