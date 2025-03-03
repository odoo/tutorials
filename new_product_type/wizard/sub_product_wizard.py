from odoo import  api, fields, models 


class SubProductWizard(models.TransientModel):
    _name = 'sub.product.wizard'
    _description = 'Sub Product Wizard'

    line_ids = fields.One2many("sub.product.wizard.line", 'wizard_id', string="Sub Products")
    kit_product_ids = fields.Many2many("product.product", string="Kit Products")
    sale_order_line_id = fields.Many2one("sale.order.line", string="Sale Order Line")

    @api.model
    def default_get(self, fields_list):
        res = super(SubProductWizard, self).default_get(fields_list)
        sale_order_line_id = self.env.context.get('default_sale_order_line_id')

        if sale_order_line_id:
            sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)
            sale_sub_products = []
            for order_line in sale_order_line.order_id.order_line:
                if order_line.is_sub_product and order_line.linked_line_id.id == sale_order_line_id:
                    sale_sub_products.append((0, 0, {
                        'product_id': order_line.product_id.id,
                        'quantity': order_line.product_uom_qty,
                        'price': order_line.product_id.list_price
                    }))

            if not sale_sub_products:
                default_kit_products = sale_order_line.product_template_id.kit_product_ids
                sale_sub_products = [(0, 0, {
                    'product_id': product.id,
                    'quantity': 1.0,
                    'price': product.list_price
                }) for product in default_kit_products]

            res['line_ids'] = sale_sub_products
        
        return res


    def action_confirm(self):
        self.ensure_one()
        sale_order_line_id = self.sale_order_line_id.id
        
        if not sale_order_line_id:
            return {'type': 'ir.actions.act_window_close'}

        sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)
        sale_order = sale_order_line.order_id

        existing_sub_lines = sale_order.order_line.filtered(lambda l: l.is_sub_product and l.linked_line_id.id == sale_order_line.id)
        existing_sub_product_map = {line.product_id.id: line for line in existing_sub_lines}

        current_sub_product_ids = {line.product_id.id for line in self.line_ids}
        lines_to_remove = existing_sub_lines.filtered(lambda l: l.product_id.id not in current_sub_product_ids)
        
        if lines_to_remove:
            lines_to_remove.unlink()

        sub_total_price = 0

        for line in self.line_ids:
            if line.product_id.id in existing_sub_product_map:
                existing_line = existing_sub_product_map[line.product_id.id]
                existing_line.write({'product_uom_qty': line.quantity, 'price_unit': 0.0})
            else:
                self.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'price_unit': 0.0,
                    'is_sub_product': True,
                    'linked_line_id': sale_order_line.id
                })
            
            sub_total_price += line.price * line.quantity

        sale_order_line.write({'price_unit': sub_total_price})

        return {'type': 'ir.actions.act_window_close'}
