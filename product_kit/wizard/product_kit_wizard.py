from odoo import fields, models, api

class SubproductKitWizard(models.TransientModel):
    _name = 'subproduct.kit.wizard'
    _discription = 'Sub Product Kit Wizard'

    sub_product_line_ids = fields.One2many('subproduct.kit.line', 'wizard_id')
    

    @api.model
    def default_get(self, fields_list):
        res = super(SubproductKitWizard, self).default_get(fields_list)
        product_id = self.env.context.get("default_product_template_id")
        order_id = self.env.context.get("default_sale_order_id")
        product_template = self.env['product.template'].browse(product_id)
        
        
        existing_subproduct = self.env['subproduct.kit.line'].search(
            [
                ('product_template_id', '=', product_id),
                ('order_id', '=', order_id)
            ])
        
        sub_product_lines = []
        
        if existing_subproduct:
            sub_product_lines = existing_subproduct.ids
        else:
            for sub_product in product_template.sub_products_kit_ids:
                print(sub_product.id)
                sub_product_line = self.env['subproduct.kit.line'].create({
                    'order_id': order_id,
                    'product_template_id': product_id,
                    'sub_product_id': sub_product.id,
                    'name': sub_product.name,
                    'quantity': 0,
                    'price': sub_product.list_price,
                })
                sub_product_lines.append(sub_product_line.id)

        res['sub_product_line_ids'] = [(6, 0, sub_product_lines)]
        return res

    def action_confirm(self):
        sale_order_line= self.env['sale.order.line'].search([('id','=',self.env.context.get('active_id'))])
        product_id = self.env.context.get("default_product_template_id")
        
        total_price = 0.0  
        if (len(sale_order_line.linked_product_kit_ids) == 0):
            for line in self.sub_product_line_ids:
                print(line.sub_product_id.id)
                if line.quantity > 0:  
                    self.env['sale.order.line'].create({
                        'linked_product_kit_id': sale_order_line.id,
                        'order_id': sale_order_line.order_id.id,  
                        'product_id': line.sub_product_id.id,
                        'product_template_id': product_id,  
                        'name': line.name,  
                        'product_uom_qty': line.quantity, 
                        'price_unit': 0,
                        'price_subtotal': 0,
                        
                    })
                    total_price += line.quantity * line.price

            sale_order_line.price_subtotal = total_price
        else:
            print("hello")
            for linked_line in sale_order_line.linked_product_kit_ids:
                for wizard_line in self.sub_product_line_ids:
                    if (linked_line.product_id == wizard_line.sub_product_id):
                        linked_line.write({
                            'product_uom_qty': wizard_line.quantity,
                            'price_unit': 0,
                            'price_subtotal': wizard_line.quantity * wizard_line.price,
                        })
                        total_price += wizard_line.quantity * wizard_line.price

        sale_order_line.price_subtotal = total_price

        return {'type': 'ir.actions.act_window_close'}


    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}
    


class SubproductKitLine(models.TransientModel):
    _name = 'subproduct.kit.line'
    _description = 'Sub Product Kit Line'

    wizard_id = fields.Many2one('subproduct.kit.wizard', string="Wizard", ondelete='cascade')
    name = fields.Char(string="Product Name")
    quantity = fields.Integer(string="Quantity", default=1)
    price = fields.Float(string="Price", default=0.0)
    sub_product_id = fields.Many2one('product.product')
    product_template_id = fields.Many2one('product.template')
    order_id = fields.Many2one('sale.order')
