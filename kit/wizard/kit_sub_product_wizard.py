from odoo import fields, models


class KitSubProductWizard(models.TransientModel):
    _name = "kit.sub.product.wizard"

    sub_product_lines_id = fields.One2many('kit.sub.product.line.wizard', 'sub_product_id')

    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        active_id = self._context.get('active_id')
        sale_order_line = self.env['sale.order.line'].browse(active_id)
        sale_order = sale_order_line.order_id
        sub_product_lines = []
        for sub_product in sale_order_line.product_id.sub_products_ids:
            existing_sale_order_line = sale_order.order_line.filtered(lambda line:line.product_id.id == sub_product.id and line.parent_id.id == sale_order_line.id)
            if existing_sale_order_line:
                sub_product_lines.append((0,0,{
                    'product_id': existing_sale_order_line.product_id.id,
                    'quantity': existing_sale_order_line.product_uom_qty,
                    'price': existing_sale_order_line.kit_price,
                    'sale_order_line_id':existing_sale_order_line.id
                }))
            else:
                sub_product_lines.append((0,0,{
                    'product_id': sub_product.id,
                    'price': sub_product.list_price,
                }))
        defaults['sub_product_lines_id'] = sub_product_lines
        return defaults

    def action_confirm(self):
        active_id = self._context.get('active_id')
        sale_order_line = self.env['sale.order.line'].browse(active_id)
        total_price_of_unit_product = sum(self.sub_product_lines_id.mapped(lambda x: x.quantity * x.price))
        sale_order_line.update({'price_unit': total_price_of_unit_product})
        sale_order = sale_order_line.order_id
        existing_lines = sale_order.order_line.filtered(lambda x: x.parent_id.id == sale_order_line.id)
        for lines in self.sub_product_lines_id:
            if not existing_lines:
                sale_order.order_line.create({
                        'order_id': sale_order.id,
                        'product_id' : lines.product_id.id,
                        'name': lines.product_id.name,
                        'product_uom_qty': lines.quantity,
                        'price_unit': 0,
                        'customer_lead' : 0,
                        'parent_id': sale_order_line.id,
                        'kit_price': lines.price
                })
            else:
                print(lines.sale_order_line_id.id)
                lines.sale_order_line_id.update({
                        'kit_price': lines.price,
                        'product_uom_qty': lines.quantity,
                        'price_unit': 0
                    })
