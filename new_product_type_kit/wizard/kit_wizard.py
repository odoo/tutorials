from odoo import api, Command, fields, models


class KitWizard(models.TransientModel):
    _name = 'kit.wizard'
    _description = 'Kit Wizard'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    kit_line_ids = fields.One2many('kit.wizard.line', 'wizard_id', string="Sub Products")
    sale_order_line_id = fields.Many2one('sale.order.line', string="Parent Line")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        product_id = self.env.context.get("default_product_id")
        order_id = self.env.context.get("active_id")
        sale_order_line_id = self.env.context.get("default_sale_order_line_id")

        if not product_id or not order_id:
            return res

        product = self.env["product.product"].browse(product_id)
        order = self.env["sale.order"].browse(order_id)
        sub_products = product.sub_product_ids
        lines = []

        for sub in sub_products:
            existing_line = order.order_line.filtered(
                lambda l: l.product_id.id == sub.id
                and l.kit_parent_line_id
                and l.kit_parent_line_id.id == sale_order_line_id
            )
            lines.append(Command.create({
                'product_id': sub.id,
                'quantity': existing_line.product_uom_qty if existing_line else 1.0,
                'price': existing_line.kit_unit_cost if existing_line else sub.lst_price,
            }))

        res.update({
            'product_id': product_id,
            'kit_line_ids': lines,
            'sale_order_line_id': sale_order_line_id,
        })
        return res

    def action_confirm(self):
        order_id = self.env.context.get("active_id")
        sale_order_line_id = self.env.context.get("default_sale_order_line_id")
        order = self.env["sale.order"].browse(order_id)
        parent_line = order.order_line.filtered(lambda l: l.id == sale_order_line_id)
        total_price = self.product_id.lst_price

        for line in self.kit_line_ids:
            existing_line = order.order_line.filtered(
                lambda l: l.product_id.id == line.product_id.id
                and l.kit_parent_line_id
                and l.kit_parent_line_id.id == sale_order_line_id
            )
            if existing_line:
                existing_line.write({
                    'product_uom_qty': line.quantity,
                    'kit_unit_cost': line.price,
                    'price_unit': 0,
                })
            else:
                self.env['sale.order.line'].create({
                    'order_id': order.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'kit_unit_cost': line.price,
                    'price_unit': 0.0,
                    'is_kit_component': True,
                    "sequence": parent_line.sequence,
                    'kit_parent_line_id': sale_order_line_id,
                    # 'name': product.name,
                })

            total_price += line.quantity * line.price
        parent_line.write({"price_unit": total_price})
