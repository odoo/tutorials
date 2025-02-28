from odoo import api, fields, models

class SubProductWizard(models.TransientModel):
    _name = "sub.product.wizard"
    _description = "Wizard to add sub-products"

    sub_product_ids = fields.One2many(comodel_name='sub.product.line.wizard', inverse_name='wizard_id', string="Sub Products")
    order_id = fields.Many2one('sale.order', string="Sale Order")

    @api.onchange('order_id')
    def _onchange_order_id(self):
        if self.order_id and not self.order_id.id:
            raise UserError("Please save the order before adding sub-products.")

    @api.model
    def default_get(self, fields_list):
        res = super(SubProductWizard, self).default_get(fields_list)
        active_id = self.env.context.get('active_id')

        if active_id:
             main_line = self.env['sale.order.line'].browse(active_id)
             order = main_line.order_id
             existing_sub_products = self.env['sale.order.line'].search([
                 ('order_id', '=', order.id),
                 ('sequence', '>', main_line.sequence)  
             ])
             sub_products = []
             if existing_sub_products:
                for line in existing_sub_products:
                    sub_products.append((0, 0, {
                       'product_id': line.product_id.id,
                       'quantity': line.product_uom_qty,
                       'price': line.price_unit,
                    }))
             else:
                 if main_line.product_id and main_line.product_template_id.is_kit:
                     for sub_product in main_line.product_template_id.sub_products_ids:
                         sub_products.append((0, 0, {
                           'product_id': sub_product.id,
                           'quantity': 1.0,
                           'price': sub_product.lst_price,
                         }))
             res['sub_product_ids'] = sub_products
        return res
                   
    def action_add_products(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            main_line = self.env['sale.order.line'].browse(active_id)
            order = main_line.order_id
            sequence = main_line.sequence + 1 
            for line in self.sub_product_ids:
                self.env['sale.order.line'].create({
                    'order_id': order.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'price_unit': line.price,
                    'sequence': sequence,
                })
                sequence += 1 
        return {'type': 'ir.actions.act_window_close'}