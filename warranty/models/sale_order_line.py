from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    warranty_product_id = fields.Many2one('product.template', string='Warranty')

    def unlink(self):
        removable_order_lines = self.env['sale.order.line'].search([
            ('order_id', '=', self.order_id.id),
            ('warranty_product_id', '=', self.product_template_id.id)
        ])
        if removable_order_lines:
            removable_order_lines.unlink()
        return super().unlink()
