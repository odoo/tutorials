from odoo import api, Command, fields, models


class WarrantyProduct(models.TransientModel):
    _name = 'kit.wizard'
    _description = 'Kit wizard description'

    name = fields.Char()
    wizard_product_ids = fields.One2many(
        'product.wizard',
        'wizard_kit_id'
    )
    wizard_product_template_id = fields.Many2one('product.template')

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        vals_list = []

        sub_products = self.env['sale.order.line'].browse(self.env.context['active_id']).product_template_id.sub_products_ids
        existing_sale_order_lines = self.env['sale.order.line'].search([('parent_id','=', self.env.context['active_id'])])

        if existing_sale_order_lines:
            for so_line in existing_sale_order_lines:
                curr_product = self.env['product.wizard'].create(
                    {
                        'product_id': so_line.product_id.id,
                        'price': so_line.secondary_price_unit,
                        'quantity': so_line.product_uom_qty,
                        'sale_order_line_id': self.env.context['active_id'],
                    }
                )
                vals_list.append(Command.link(curr_product.id))
        else:
            for product in sub_products:
                curr_product = self.env['product.wizard'].create(
                    {
                        'product_id': product.id,
                        'price': product.lst_price,
                        'sale_order_line_id': self.env.context['active_id'],
                    }
                )
                vals_list.append(Command.link(curr_product.id))
    
        res['wizard_product_ids'] = vals_list
        return res

    def add_sub_products_to_sale_order_line(self):
        sale_order_ln = self.env['sale.order.line'].browse(self.env.context['active_id'])
        existing_sale_order_line = self.env['sale.order.line'].search([('parent_id','=', self.env.context['active_id'])])
        total_amt = sale_order_ln.product_id.lst_price * sale_order_ln.product_uom_qty

        if existing_sale_order_line:
            existing_sub_products_dict = {line.product_id.id: line for line in existing_sale_order_line}
            for kit_product in self.wizard_product_ids:
                total_amt = total_amt + (kit_product.price * kit_product.quantity)
                existing_sub_products_dict.get(kit_product.product_id.id).write({'price_unit': 0, 'secondary_price_unit': kit_product.price, 'product_uom_qty': kit_product.quantity})
        else:
            for kit_product in self.wizard_product_ids:
                total_amt = total_amt + (kit_product.price * kit_product.quantity)
                self.env['sale.order.line'].create(
                    {
                        'order_id': sale_order_ln.order_id.id,
                        'product_id': kit_product.product_id.id,
                        'name': kit_product.product_id.name,
                        'price_unit': 0,
                        'secondary_price_unit': kit_product.price,
                        'product_uom_qty': kit_product.quantity,
                        'parent_id': kit_product.sale_order_line_id.id,
                    }
                )
        sale_order_ln.write({'price_subtotal': total_amt})
