from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_warranty_id = fields.Many2one('product.product', string="Product Warrantry Id")

    @api.model
    def create(self, vals):
        line = super(SaleOrderLine, self).create(vals)
        if line.product_id.is_warranty_available:
            warranty_config = self.env['warranty.configuration'].search([
                ('product_id', '=', line.product_id.id)
            ], limit=1)
            if warranty_config:
                self.env['sale.order.line'].create({
                    'order_id': line.order_id.id,
                    'product_id': warranty_config.product_id.id,
                    'price_unit': (line.price_unit * warranty_config.percentage) / 100,
                    'warranty_id': warranty_config.id,
                })
        return line

    def unlink(self):
        for line in self:
            warranty_lines = self.env['sale.order.line'].search([
                ('product_warranty_id', '=', line.product_id.id)
            ])
            # print(warranty_lines)


            if warranty_lines:
                warranty_lines.unlink()

        # Delete the main product line
        return super(SaleOrderLine, self).unlink()

