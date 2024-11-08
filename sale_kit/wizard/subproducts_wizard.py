from odoo import Command, fields, models


class SubproductWizard(models.TransientModel):
    _name = 'subproduct.wizard'
    _description = 'Select the subproducts'

    name = fields.Char()
    subproduct_ids = fields.One2many(comodel_name='product.wizard', inverse_name='subproduct_id')

    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        sale_order_line = self.env['sale.order.line'].browse(active_id)

        sale_order = self.env['sale.order'].browse(sale_order_line.order_id.id)
        subproducts_list = []
        for line in sale_order.order_line:
            if line.parent_sale_order_line_id.id==active_id and (line.product_id.id in sale_order_line.product_id.sub_products_ids.ids):
                subproducts_list.append(Command.create({'product_id': line.product_id.id, 'quantity': line.product_uom_qty, 'price': line.subproduct_price}))

        if len(subproducts_list)==(len(sale_order_line.product_id.sub_products_ids)):
            values['subproduct_ids'] = subproducts_list
            return values

        added_subproducts = []
        for sub_product in subproducts_list:
            added_subproducts.append(sub_product[2]['product_id'])

        product = sale_order_line.product_id.sub_products_ids
        for prop in product:
            if prop.id not in added_subproducts: 
                subproducts_list.append(Command.create({'product_id': prop.id, 'quantity': 0, 'price': prop.list_price}))
        values['subproduct_ids'] = subproducts_list
        return values

    def action_add_subproducts(self):
        for record in self:
            active_id = self.env.context.get('active_id')
            sale_order_line = self.env['sale.order.line'].browse(active_id)
            sub_products_line = self.env['sale.order.line'].search([('parent_sale_order_line_id', '=', active_id)])

            sub_product_line_dict = {line.product_id.id: line for line in sub_products_line}
            total_price = 0
            for sub_product in record.subproduct_ids:
                if sub_product.product_id.id in sub_products_line.mapped('product_id.id'):
                    line = sub_product_line_dict.get(sub_product.product_id.id)
                    line.write({
                                'product_uom_qty':sub_product.quantity,
                                'price_unit': 0,
                                'subproduct_price': sub_product.price
                            })
                    total_price = total_price + sub_product.price*sub_product.quantity
                else:
                    self.env['sale.order.line'].create({
                        'order_id': sale_order_line.order_id.id,
                        'product_id': sub_product.product_id.id,
                        'name': sub_product.product_id.name,
                        'product_uom_qty': sub_product.quantity,
                        'price_unit': 0,
                        'subproduct_price': sub_product.price,
                        'product_uom':sub_product.product_id.uom_id.id,
                        'parent_sale_order_line_id': sale_order_line.id
                    })
                    total_price = total_price + sub_product.price * sub_product.quantity

            sale_order_line.write({
                'price_unit': sale_order_line.product_id.list_price*sale_order_line.product_uom_qty + total_price
            })
