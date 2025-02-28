from odoo import models, fields, api

class SubProductWizard(models.TransientModel):
    _name = 'sub.product.wizard'
    _description = 'Sub Product Wizard'

    line_ids = fields.One2many("sub.product.wizard.line", 'wizard_id', string="Sub Products")
    kit_product_ids = fields.Many2many("product.product", string="Kit Products")

    @api.model
    def default_get(self, fields_list):
        res = super(SubProductWizard, self).default_get(fields_list)
        sale_order_line_id = self.env.context.get('sale_order_line_id') 
        if sale_order_line_id:
            sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)
            sub_products = sale_order_line.product_template_id.kit_product_ids  
            line_values = [(0, 0, {'product_id': product.id, 'quantity': 1.0 ,'price':product.list_price }) for product in sub_products]

            res['line_ids'] = line_values 
        return res


    def action_confirm(self):
        """This method moves wizard lines to sale.order.line when user confirms."""
        self.ensure_one()  # Ensure only one wizard is processed at a time

        active_id = self.env.context.get('active_id')
        
        if active_id:
            sale_order_line = self.env['sale.order.line'].browse(active_id)
            
            for line in self.line_ids:
                self.env['sale.order.line'].create({
                    'order_id': sale_order_line.order_id.id,  # Link to correct order
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'price_unit': 0.0,  # Sub-product price is 0 (covered by main product)
                    'is_sub_product': True,  # Custom flag for sub-products (if needed)
                })
        
        return {'type': 'ir.actions.act_window_close'}  # Close wizard after confirmation

