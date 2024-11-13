from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_kit = fields.Boolean(related='product_template_id.is_kit', store=True)
    parent_id = fields.Many2one('sale.order.line', ondelete='cascade')
    secondary_price_unit = fields.Float()

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_price_unit(self):
        for record in self:
            super()._compute_price_unit()
            sub_products_so_lines = self.env['sale.order.line'].search([('parent_id', '=', record._origin.id)])
            total_price = 0
            for so_line in sub_products_so_lines:
                total_price = total_price + (so_line.secondary_price_unit * so_line.product_uom_qty)
            record.price_unit = record.price_unit + total_price
