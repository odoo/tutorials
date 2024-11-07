from odoo import fields, models, api


class SubProducts(models.TransientModel):
    _name = 'sub.products'
    _description = "Sub Product"

    sub_product_line_ids = fields.One2many('sub.products.line', 'sub_product_id')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        record = self.env["sale.order.line"].browse(active_id)
        sub_product_lines = []
        for sub_product in record.product_template_id.sub_product_ids:
            sub_product_lines.append((0, 0, {'product_id' : sub_product.id}))
        res['sub_product_line_ids'] = sub_product_lines
        return res
    
    def action_add_sub_product(self):
        active_id = self.env.context.get('active_id')
        product_order_line = self.env["sale.order.line"].browse(active_id)
        new_price_unit = product_order_line.product_uom_qty * product_order_line.price_unit
        for sub_product_line in self.sub_product_line_ids:
            self.env['sale.order.line'].create(
                {
                    'order_id': product_order_line.order_id.id,
                    'product_id': sub_product_line.product_id.id,
                    'name': sub_product_line.product_id.name,
                    'product_uom_qty': sub_product_line.quantity,
                    'price_unit': 0.0,
                    'customer_lead': 0.0
                }
            )
            new_price_unit = new_price_unit + sub_product_line.quantity * sub_product_line.price
        product_order_line.price_unit = new_price_unit
