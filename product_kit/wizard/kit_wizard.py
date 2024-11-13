from odoo import api, Command, fields, models


class WarrantyProduct(models.TransientModel):
    _name = 'kit.wizard'
    _description = 'Kit wizard description'

    name = fields.Char()
    wizard_product_ids = fields.One2many(
        'product.wizard',
        'wizard_kit_id'
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        sub_products = self.env['sale.order.line'].browse(self.env.context['active_id']).product_template_id.sub_products_ids
        existing_so_line = self.env['sale.order.line'].search([('parent_id', '=', self.env.context['active_id'])])
        existing_so_line_dict = {so_line.product_id.id: so_line for so_line in existing_so_line}
        vals_list = []

        for product in sub_products:
            if product.id in existing_so_line_dict:
                so_line = existing_so_line_dict.get(product.id)
                curr_product = self.env['product.wizard'].create(
                    {
                        'product_id': so_line.product_id.id,
                        'price': so_line.secondary_price_unit,
                        'quantity': so_line.product_uom_qty,
                        'sale_order_line_id': self.env.context['active_id']
                    }
                )
                vals_list.append(Command.link(curr_product.id))
            else:
                curr_product = self.env['product.wizard'].create(
                    {
                        'product_id': product.id,
                        'price': product.lst_price,
                        'sale_order_line_id': self.env.context['active_id']
                    }
                )
                vals_list.append(Command.link(curr_product.id))
        res['wizard_product_ids'] = vals_list
        return res

    def add_sub_products_to_sale_order_line(self):
        for record in self:
            existing_so_line = self.env['sale.order.line'].search([('parent_id', '=', self.env.context['active_id'])])
            existing_so_line_dict = {so_line.product_id.id: so_line for so_line in existing_so_line}

            for kit_product in record.wizard_product_ids:
                if kit_product.product_id.id in existing_so_line_dict:
                    existing_so_line_dict.get(kit_product.product_id.id).write({'price_unit': 0, 'secondary_price_unit': kit_product.price, 'product_uom_qty': kit_product.quantity})
                else:
                    self.env['sale.order.line'].create(
                        {
                            'order_id': kit_product.sale_order_line_id.order_id.id,
                            'product_id': kit_product.product_id.id,
                            'name': kit_product.product_id.name,
                            'price_unit': 0,
                            'secondary_price_unit': kit_product.price,
                            'product_uom_qty': kit_product.quantity,
                            'parent_id': kit_product.sale_order_line_id.id,
                        }
                    )
