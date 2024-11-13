from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    is_kit = fields.Boolean(compute="_compute_product_is_kit")
    parent_id = fields.Many2one('sale.order.line', ondelete='cascade')
    kit_price = fields.Float()

    @api.depends('product_id.is_kit')
    def _compute_product_is_kit(self):
        for records in self:
            records.is_kit = records.product_id.is_kit

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_price_unit(self):
        super()._compute_price_unit()
        for line in self:
            if line.is_kit:
                sub_product_lines = line.order_id.order_line.filtered(lambda l: l.parent_id.id == line._origin.id)
                price_unit = sum(sub_product_line.kit_price * sub_product_line.product_uom_qty for sub_product_line in sub_product_lines)
                line.price_unit = price_unit

    def action_wizard_of_sub_product(self):
        return {
            'name': (f'Product: {self.product_id.name}'),
            'type': 'ir.actions.act_window',
            'res_model': 'kit.sub.product.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
