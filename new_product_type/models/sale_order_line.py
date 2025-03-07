from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_kit = fields.Boolean(related='product_id.is_kit')
    parent_line_id = fields.Many2one('sale.order.line', ondelete='cascade')
    is_subproduct = fields.Boolean(default=False, store=True)

    def unlink(self):
        # Find all child lines in a single query and unlink them efficiently
        child_lines = self.env['sale.order.line'].search([
            ('parent_line_id', 'in', self.filtered(lambda l: l.product_id.is_kit).ids)
        ])
        if child_lines:
            child_lines.unlink()
        return super(SaleOrderLine, self).unlink()

    def write(self, vals):
        result = super(SaleOrderLine, self).write(vals)
        if vals.get('product_template_id'):
            for line in self:
                product_template = self.env['product.template'].browse(vals.get('product_template_id'))
                # Update price in a separate write to avoid recursion
                line.price_unit = product_template.list_price
                # Delete child lines in a single operation
                child_lines = self.env['sale.order.line'].search([('parent_line_id', '=', line.id)])
                if child_lines:
                    child_lines.unlink()
        return result
