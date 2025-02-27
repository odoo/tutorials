from odoo import api, fields, models

class ProductSubWizard(models.TransientModel):
    _name = "product.sub.wizard"
    _description = "Wizard to manage sub-products"

    product_id = fields.Many2one('product.product', string="Product", required=True)
    line_ids = fields.One2many('product.sub.wizard.line', 'wizard_id', string="Sub Products")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_order_line_id = self.env.context.get('sale_order_line_id')

        if sale_order_line_id:
            sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)
            sale_order = sale_order_line.order_id
            product = sale_order_line.product_id.product_tmpl_id
            
            existing_wizard = self.env['product.sub.wizard'].search([('product_id', '=', product.id)])
            sale_order_product_ids = {line.product_id.id for line in sale_order.order_line}
            unique_product_ids = set()

            # Combine both operations in a single list comprehension
            sub_products = []
            
            # Add existing sub-products first
            for line in existing_wizard.line_ids:
                if line.product_id.id not in unique_product_ids and line.product_id.id in sale_order_product_ids:
                    sub_products.append((0, 0, {
                        'product_id': line.product_id.id,
                        'quantity': line.quantity,
                        'price': line.price,
                    }))
                    unique_product_ids.add(line.product_id.id)
            
            # Add default sub-products
            for sub_product in product.sub_product_ids:
                if sub_product.id not in sale_order_product_ids and sub_product.id not in unique_product_ids:
                    sub_products.append((0, 0, {
                        'product_id': sub_product.id,
                        'quantity': 1,
                        'price': sub_product.list_price,
                    }))
                    unique_product_ids.add(sub_product.id)

            res.update({
                'product_id': product.id,
                'line_ids': sub_products
            })

        return res

    def action_confirm_sub_products(self):
        sale_order_line_id = self.env.context.get('sale_order_line_id')
        sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)

        if not sale_order_line:
            return False
        
        sub_product_total = sum(sub_product.price * sub_product.quantity for sub_product in self.line_ids)
        sale_order = sale_order_line.order_id
        
        existing_sub_lines = sale_order.order_line.filtered(lambda l: l.kit_main_product_id.id == sale_order_line.id)
        existing_sub_product_map = {line.product_id.id: line for line in existing_sub_lines}

        # Create a batch of new lines to add
        sub_product_lines = []
        for sub_product in self.line_ids:
            if sub_product.product_id.id not in existing_sub_product_map:
                sub_product_lines.append(({
                    'order_id': sale_order.id, 
                    'product_id': sub_product.product_id.id,
                    'product_uom_qty': sub_product.quantity,
                    'price_unit': 0,
                    'kit_main_product_id': sale_order_line.id,
                    'sequence': sale_order_line.sequence
                }))

        if sub_product_lines:
            self.env['sale.order.line'].create(sub_product_lines)
        
        # Update existing sub-product lines in a single operation
        for sub_product in self.line_ids:
            if sub_product.product_id.id in existing_sub_product_map:
                existing_sub_product_map[sub_product.product_id.id].write({
                    'product_uom_qty': sub_product.quantity,
                    'price_unit': 0,
                })
        
        # Update wizard
        product_id = sale_order_line.product_id.product_tmpl_id.id
        existing_wizard = self.env['product.sub.wizard'].search([('product_id', '=', product_id)])
        existing_wizard.line_ids = self.line_ids

        # Update price
        sale_order_line.price_unit = sub_product_total

        return True

