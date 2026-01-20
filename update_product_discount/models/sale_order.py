from odoo import api, fields, models, Command

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    global_discount_removed = fields.Boolean(default=False, string="Global Discount Manually Removed")
    global_discount_applied = fields.Boolean(default=False, string="Global Discount Applied")

    def _update_global_discount(self):
        for order in self:
            if order.global_discount_removed:
                return
            discount_product = order.company_id.sale_discount_product_id
            discount_lines = order.order_line.filtered(lambda l: l.product_id == discount_product)
            if not discount_lines:
                return
            non_discount_lines = order.order_line.filtered(lambda l: l.product_id != discount_product and not l.display_type)
            if not non_discount_lines:
                discount_lines.unlink()
                return
            discount_wizard = self.env['sale.order.discount'].search([
                ('sale_order_id', '=', order.id),
                ('discount_type', '=', 'so_discount')
            ], limit=1)
            discount_percentage = discount_wizard.discount_percentage if discount_wizard else 0.0
            discount_lines.unlink()
            if discount_percentage:
                discount_amount = sum(line.price_subtotal for line in non_discount_lines) * discount_percentage
                order.order_line.create({
                    'order_id': order.id,
                    'product_id': discount_product.id,
                    'price_unit': -discount_amount,
                    'tax_id': [Command.set(order.fiscal_position_id.map_tax(discount_product.taxes_id).ids)],
                    'sequence': 999,
                    'name': f"Global Discount ({discount_percentage * 100}%)"
                })

    def write(self, vals):
        for order in self:
            if 'order_line' in vals:
                discount_product = order.company_id.sale_discount_product_id
                discount_lines = order.order_line.filtered(lambda l: l.product_id == discount_product)
                discount_removed_manually = any(
                    isinstance(line, (tuple, list)) and line[0] == 2 and line[1] in discount_lines.ids
                    for line in vals.get('order_line', [])
                )
                if discount_removed_manually:
                    vals['global_discount_removed'] = True
        res = super().write(vals)

        for order in self:
            discount_product = order.company_id.sale_discount_product_id
            discount_lines = order.order_line.filtered(lambda l: l.product_id == discount_product)
            non_discount_lines = order.order_line.filtered(lambda l: l.product_id != discount_product and not l.display_type)
            if not non_discount_lines and discount_lines:
                discount_lines.unlink()
            elif discount_lines:
                order._update_global_discount()
        return res

    @api.model_create_multi
    def create(self, vals):
        order = super().create(vals)
        discount_product = order.company_id.sale_discount_product_id
        discount_wizard = self.env['sale.order.discount'].search([
            ('sale_order_id', '=', order.id),
            ('discount_type', '=', 'so_discount')
        ], limit=1)
        if discount_wizard:
            order.global_discount_applied = True
            order._update_global_discount()
        discount_lines = order.order_line.filtered(lambda l: l.product_id == discount_product)
        non_discount_lines = order.order_line.filtered(lambda l: l.product_id != discount_product and not l.display_type)
        if not non_discount_lines and discount_lines:
            discount_lines.unlink()
        return order
