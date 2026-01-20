from odoo import api, fields, models

class SubproductWizard(models.TransientModel):
    _name = 'subproduct'
    _description = 'Sub-product Wizard'

    product_id = fields.Many2one('product.product', string="Product", required=True)
    sub_product_ids = fields.One2many('subproduct.line', 'kit_product_line_id')
    order_line_id = fields.Many2one('sale.order.line')

    @api.model
    def default_get(self, fields):
        res = super(SubproductWizard, self).default_get(fields)

        product_id = self.env.context.get('default_product_id')
        order_line_id = self.env.context.get('default_order_line_id')
        product = self.env['product.product'].browse(product_id)
        sub_products = self.env['subproduct'].search(
            [('order_line_id', '=', order_line_id),
            ('product_id', '=', product_id)], 
            order='id desc', limit=1)

        sub_products_list = []
        
        if sub_products.exists():
            for subproduct, selected_product in zip(sub_products.sub_product_ids, product.kit_product_ids):
                sub_products_list.append((0, 0, {
                        'product_id': selected_product.id,
                        'kit_product_name': selected_product.product_tmpl_id.name,
                        'kit_product_qty': subproduct.kit_product_qty,
                        'kit_product_price': subproduct.kit_product_price
                    }))
        else:
            for selected_product in product.kit_product_ids:
                sub_products_list.append((0, 0, {
                        'product_id': selected_product.id,
                        'kit_product_name': selected_product.product_tmpl_id.name,
                        'kit_product_qty': 1.0,
                        'kit_product_price': selected_product.list_price,
                    })) 
        
        res['sub_product_ids'] = sub_products_list
        return res


    def action_confirm_subproduct(self):
        order_line = self.env['sale.order.line'].search([('id', '=', self.order_line_id.id)])
        product = self.env['product.product'].browse(self.product_id.id)
        order_line_subproduct = self.env['sale.order.line'].search(
            [('order_id', '=', order_line.order_id.id),
            ('parent_product_id', '=', self.product_id.id)])
        
        total = 0
        if order_line_subproduct.exists():
            for sub_product_data, order_line_rec in zip(self.sub_product_ids, order_line_subproduct):
                total += (sub_product_data.kit_product_price * sub_product_data.kit_product_qty)

                order_line_rec.product_uom_qty = sub_product_data.kit_product_qty
                order_line_rec.price_unit = 0
        else:
            for sub_product_data, selected_products  in zip(self.sub_product_ids, product.kit_product_ids):
                total += (sub_product_data.kit_product_price * sub_product_data.kit_product_qty)

                self.env['sale.order.line'].create({
                'order_id': order_line.order_id.id,
                'product_id': selected_products.id,
                'name': selected_products.product_tmpl_id.name,
                'price_unit': 0,
                'product_uom_qty': sub_product_data.kit_product_qty,
                'parent_product_id': self.product_id.id,
                'is_subproduct': True,
                'sequence': order_line.sequence
                })
                
        order_line.price_unit = total + product.product_tmpl_id.list_price
    

