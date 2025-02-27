from odoo import api, fields, models

class SubproductWizard(models.TransientModel):
    _name = 'subproduct'
    _description = 'Sub-product Wizard'

    product_id = fields.Many2one('product.product', string="Product", required=True)
    sub_product_ids = fields.One2many('subproduct.line', 'subproduct_line_id')
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
            # Update wizard data
            for subproduct, selected_product in zip(sub_products.sub_product_ids, product.selected_product_ids):
                sub_products_list.append((0, 0, {
                        'product_id': selected_product.id,
                        'sub_product_name': selected_product.product_tmpl_id.name,
                        'quantity': subproduct.quantity,
                        'unit_price': subproduct.unit_price
                    }))
        else:
            # New Data
            for selected_product in product.selected_product_ids:
                sub_products_list.append((0, 0, {
                        'product_id': selected_product.id,
                        'sub_product_name': selected_product.product_tmpl_id.name,
                        'quantity': 1.0,
                        'unit_price': selected_product.list_price,
                    })) 
        
        res['sub_product_ids'] = sub_products_list
        return res

    #=== ACTION METHOD ===#    

    def action_confirm_subproduct(self):
        order_line = self.env['sale.order.line'].search([('id', '=', self.order_line_id.id)])
        product = self.env['product.product'].browse(self.product_id.id)
        order_line_subproduct = self.env['sale.order.line'].search(
            [('order_id', '=', order_line.order_id.id),
            ('parent_product_id', '=', self.product_id.id)])
        
        total = 0
        if order_line_subproduct.exists():
            # Update Order-line
            for sub_product_data, order_line_rec in zip(self.sub_product_ids, order_line_subproduct):
                total += (sub_product_data.unit_price * sub_product_data.quantity)

                order_line_rec.product_uom_qty = sub_product_data.quantity
                order_line_rec.price_unit = 0
        else:
            # Create Order-line
            for sub_product_data, selected_products  in zip(self.sub_product_ids, product.selected_product_ids):
                total += (sub_product_data.unit_price * sub_product_data.quantity)

                self.env['sale.order.line'].create({
                'order_id': order_line.order_id.id,
                'product_id': selected_products.id,
                'name': selected_products.product_tmpl_id.name,
                'price_unit': 0,
                'product_uom_qty': sub_product_data.quantity,
                'parent_product_id': self.product_id.id,
                'is_subproduct': True,
                'sequence': order_line.sequence
                })
                
        order_line.price_unit = total + product.product_tmpl_id.list_price
    

class SubproductWizardLine(models.TransientModel):
    _name = 'subproduct.line'
    _description = 'Sub-product Wizard Line'

    subproduct_line_id = fields.Many2one('subproduct')
    product_id = fields.Many2one('product.product')
    sub_product_name = fields.Char(string="Product Name")
    quantity = fields.Integer(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
