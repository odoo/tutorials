from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def unlink(self):
        """Ensure that when a product is deleted, its warranty is also removed."""
        warranty_lines_to_delete = self.env['sale.order.line']

        for line in self:
            if not line.product_template_id:
                continue

            warranty_product = line.product_id.product_tmpl_id.warranty_id.product_id

            if warranty_product:
                warranty_line = self.env['sale.order.line'].search([
                    ('order_id', '=', line.order_id.id),
                    ('product_template_id', '=', warranty_product.id),
                ], limit=1)

                warranty_lines_to_delete |= warranty_line

            warranty_lines_to_delete |= line

        return super(SaleOrderLine, warranty_lines_to_delete).unlink()
