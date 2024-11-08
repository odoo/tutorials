from odoo import api, fields, models, Command


class SubProductWizard(models.TransientModel):
    _name = 'sub.product.wizard'
    _description = 'All sub products in wizard'

    name = fields.Char()
    sub_product_ids = fields.One2many('sub.product.add.line', 'sub_product_id')

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        vals = []
        # get active ids for that sale
        sale_order_line_id = self.env.context['active_id']
        # get product lines which has those ids
        sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)
        # get those sub product ids
        sub_products = sale_order_line.product_template_id.sub_product_ids
        # search if some sub product already exists
        old_sale_order_line = self.env['sale.order.line'].search([('parent_id', '=', sale_order_line_id)])

        if old_sale_order_line:
            for old in old_sale_order_line:
                val = self.env['sub.product.add.line'].create(
                    {
                        'product_id': old.product_id.id,
                        'price':old.kit_price,
                        'quantity':old.product_uom_qty,
                        'sale_order_line_id':sale_order_line_id
                    }
                )
                vals.append(Command.link(val.id))
        else:
            for new in sub_products:
                val = self.env['sub.product.add.line'].create(
                    {
                        'product_id': new.id,
                        'price':new.lst_price,
                        'sale_order_line_id':sale_order_line_id
                    }
                )
                vals.append(Command.link(val.id))
        res["sub_product_ids"] = vals
        return res

    def add_sub_products_to_order_line(self):
        sale_order_line_id = self._context.get('active_id')
        sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)
        all_sub_product_price = sum(self.sub_product_ids.mapped(lambda tsum: tsum.quantity * tsum.price))
        final_price = all_sub_product_price + sale_order_line.product_template_id.list_price
        sale_order_line.update({'price_unit': final_price})

        old_sale_order_line = self.env['sale.order.line'].search([('parent_id', '=', sale_order_line_id)])
        if old_sale_order_line:
            self.env['sale.order.line'].search([('parent_id', '=', sale_order_line_id)]).unlink()

        sale_order = sale_order_line.order_id
        for record in self.sub_product_ids:
            sale_order.order_line.create({
                    'order_id': sale_order.id,
                    'product_id' : record.product_id.id,
                    'name': record.product_id.name,
                    'product_uom_qty': record.quantity,
                    'price_unit': 0,
                    'customer_lead' : 0,
                    'kit_price': record.price,
                    'parent_id': record.sale_order_line_id.id
            })
