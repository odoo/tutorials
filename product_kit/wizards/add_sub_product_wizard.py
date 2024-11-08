from odoo import api, Command, fields, models


class AddSubProduct(models.TransientModel):
    _name = 'add.sub.product.wizard'
    _description = 'All sub products in wizard'

    sub_product_ids = fields.One2many('add.sub.product.line', 'sub_product_id')

    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        active_id = self._context.get('active_id')
        sale_order_line = self.env['sale.order.line'].browse(active_id)
        sale_order = sale_order_line.order_id
        sub_product_lines = []
        if not any(line.parent_id.id == sale_order_line.id for line in sale_order.order_line):
            sub_products = sale_order_line.product_id.sub_products
            for sub_product in sub_products:
                sub_product_lines.append((0,0,{
                    'product_id': sub_product.id,
                    'price': sub_product.list_price
                }))
            defaults['sub_product_ids'] = sub_product_lines
        else:
            lines = sale_order_line.order_id.order_line.filtered(lambda line: line.parent_id.id == sale_order_line.id)
            for line in lines:
                sub_product_lines.append((0,0,{
                    'product_id': line.product_id.id,
                    'quantity': line.product_uom_qty,
                    'price': line.kit_price
                }))
            defaults['sub_product_ids'] = sub_product_lines
        return defaults

    def action_confirm(self):
        active_id = self._context.get('active_id')
        sale_order_line = self.env['sale.order.line'].browse(active_id)
        total_price_of_unit_product = sum(self.sub_product_ids.mapped(lambda x: x.quantity * x.price))
        main_product_total_price = sale_order_line.price_unit + total_price_of_unit_product
        sale_order_line.update({'price_unit': main_product_total_price})
        sale_order = sale_order_line.order_id
        existing_sub_lines = sale_order.order_line.filtered(lambda line: line.parent_id.id == sale_order_line.id)
        for lines in self.sub_product_ids:
            matching_line = existing_sub_lines.filtered(lambda x: x.product_id == lines.product_id)
        if matching_line:
            matching_line.write({
                'product_uom_qty': lines.quantity,
                'kit_price': lines.price
            })
        else:
            sale_order.order_line.create({
                'order_id': sale_order.id,
                'product_id': lines.product_id.id,
                'name': lines.product_id.name,
                'product_uom_qty': lines.quantity,
                'price_unit': 0,
                'customer_lead': 0,
                'parent_id': sale_order_line.id,
                'kit_price': lines.price
            })

        if sale_order.include_sub_products_in_report:
            for order_line in sale_order.order_line.filtered(lambda line: line.parent_id):
                self.env['account.move.line'].create({
                    'move_id': sale_order.invoice_ids.id,
                    'product_id': order_line.product_id.id,
                    'name': order_line.name,
                    'quantity': order_line.product_uom_qty,
                    'price_unit': order_line.kit_price,
                    'account_id': order_line.product_id.product_tmpl_id.account_id.id,
                    'tax_ids': [(6, 0, order_line.tax_id.ids)],
                })
