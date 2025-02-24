from odoo import api,fields, models,Command


class AddSubProductWizard(models.TransientModel):
    _name = 'wizard.add.sub.products'
    _description = 'Wizard for Adding Sub Products'

    def _default_sub_products(self):
        sale_order_line_id = self.env.context.get('active_id')
        if not sale_order_line_id:
            return []
        sub_product_ids = self.env['wizard.sub.product.line'].create_temp_lines()

        return [(6, 0, [line.id for line in sub_product_ids])]

    sub_line_ids = fields.One2many('wizard.sub.product.line', 'wizard_id', default=_default_sub_products)

    def action_add_sub_products(self):
        sale_order_line_id = self.env.context.get('active_id')
        sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)
        
        if not sale_order_line:
            return

        sale_order = sale_order_line.order_id
        total = 0
        all_lines = self.mapped("sub_line_ids")

        for line in all_lines:
            existing_lines = self.env['sale.order.line'].search([('parent_line_id','=',sale_order_line.id),('order_id','=',sale_order.id),('product_id','=',line.product_id.id)])
            
            if existing_lines:
                    for existing_line in existing_lines:
                       existing_line.product_uom_qty += line.product_uom_qty  
                       total += (existing_line.product_uom_qty * line.price_unit)
                       existing_line.price_unit=0
            else:
                self.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'name': line.product_id.name,  
                    "product_id": line.product_id.id,
                    "product_template_id": line.product_id.product_tmpl_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'price_unit': 0,  
                    'parent_line_id': sale_order_line_id
                })

                total+= line.product_uom_qty * line.price_unit

        sale_order_line.price_unit = total  
        return {'type': 'ir.actions.act_window_close'}
