from odoo import fields, models, api


class SubProducts(models.TransientModel):
    _name = 'sub.products'
    _description = "Sub Product"

    name = fields.Char()
    sub_product_line_ids = fields.One2many('sub.products.line', 'sub_product_id')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        sub_product = self.env['sale.order.line'].search([('sale_order_line_id', '=', active_id)])
        sale_order_line_current_record = self.env['sale.order.line'].browse(active_id)
        sub_product_lines = []
        if len(sub_product) > 0:
            for product in sub_product:
                sub_product_lines.append((0, 0, {
                    'product_id': product.product_id.id,
                    'quantity': product.product_uom_qty,
                    'price': product.previously_set_price
                }))
        else:
            for product in sale_order_line_current_record.product_template_id.sub_product_ids:
                sub_product_lines.append((0, 0, {
                    'product_id' : product.id,
                    'quantity': 1.0,
                    'price': product.lst_price
                }))
        res['sub_product_line_ids'] = sub_product_lines
        return res
    
    def action_add_sub_product(self):
        active_id = self.env.context.get('active_id')
        sub_product = self.env['sale.order.line'].search([('sale_order_line_id', '=', active_id)])
        if len(sub_product) > 0:
            self.env['sale.order.line'].search([('sale_order_line_id', '=', active_id)]).unlink()
        product_order_line = self.env['sale.order.line'].browse(active_id)
        new_price_unit = product_order_line.product_id.lst_price
        for sub_product_line in self.sub_product_line_ids:
            self.env['sale.order.line'].create(
                {
                    'order_id': product_order_line.order_id.id,
                    'product_id': sub_product_line.product_id.id,
                    'name': sub_product_line.product_id.name,
                    'product_uom_qty': sub_product_line.quantity,
                    'price_unit': 0.0,
                    'customer_lead': 0.0,
                    'sale_order_line_id': active_id,
                    'previously_set_price': sub_product_line.price
                }
            )
            new_price_unit = new_price_unit + sub_product_line.quantity * sub_product_line.price
        product_order_line.price_unit = new_price_unit
