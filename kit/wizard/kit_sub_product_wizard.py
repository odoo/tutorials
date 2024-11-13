from odoo import fields, models


class KitSubProductWizard(models.TransientModel):
    _name = "kit.sub.product.wizard"
    _description = 'This wizard is for sub product in product'
    
    sub_product_lines_id = fields.One2many('kit.sub.product.line.wizard', 'sub_product_id')

    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        active_id = self._context.get('active_id')
        sale_order_line = self.env['sale.order.line'].browse(active_id)
        sub_product_lines = []
        for sub_product in sale_order_line.product_id.sub_products_ids:
            existing_line = sale_order_line.order_id.order_line.filtered(
                lambda line: line.product_id == sub_product and line.parent_id == sale_order_line
            )

            sub_product_lines.append((0, 0, {
                'product_id': existing_line.product_id.id if existing_line else sub_product.id,
                'quantity': existing_line.product_uom_qty if existing_line else 0,
                'price': existing_line.kit_price if existing_line else sub_product.list_price,
                'sale_order_line_id': existing_line.id if existing_line else False,
            }))

        defaults['sub_product_lines_id'] = sub_product_lines
        return defaults

    def action_confirm(self):
        active_id = self._context.get('active_id')
        sale_order_line = self.env['sale.order.line'].browse(active_id)
        total_price = sum(line.quantity * line.price for line in self.sub_product_lines_id)
        sale_order_line.write({'price_unit': total_price})

        for line in self.sub_product_lines_id:
            if line.sale_order_line_id:
                line.sale_order_line_id.write({
                    'product_uom_qty': line.quantity,
                    'kit_price': line.price,
                    'price_unit': 0
                })
            else:
                sale_order_line.order_id.order_line.create({
                    'order_id': sale_order_line.order_id.id,
                    'product_id': line.product_id.id,
                    'name': line.product_id.name,
                    'product_uom_qty': line.quantity,
                    'price_unit': 0,
                    'customer_lead': 0,
                    'parent_id': sale_order_line.id,
                    'kit_price': line.price
                })
