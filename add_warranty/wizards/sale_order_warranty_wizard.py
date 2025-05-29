from dateutil.relativedelta import relativedelta
from odoo import api, Command, fields, models


class SaleOrderWarranty(models.TransientModel):
    _name = 'sale.order.warranty'
    _description = 'Add Warranty'
    
    order_line_ids = fields.Many2many(
       comodel_name='sale.order.line', 
       string="Order Lines")

    @api.model
    def default_get(self, fields_list):
        res = super(SaleOrderWarranty, self).default_get(fields_list)
        sale_order_id = self.env.context.get('active_id')
        if sale_order_id:
            sale_order = self.env['sale.order'].browse(sale_order_id)
            warranty_lines = sale_order.order_line.filtered(lambda line: line.product_template_id.is_warranty_available and not line.warranty_item)
            res['order_line_ids'] = [Command.set(warranty_lines.ids)]
        return res

    def add_warranty_to_products(self):
        self.ensure_one()
        sale_order_line = self.env["sale.order.line"]
        for record in self.order_line_ids:
            sale_order_line.create({
                'order_id': record.order_id.id,
                'price_unit': (record.warranty_item.percent/100)*record.price_unit,
                'product_id': record.warranty_item.product_id.product_variant_id.id,
                'name': f"Extended Warranty for {record.product_id.name}, Expires on: {record.end_date}",
                'related_line_id': record.id
            })
