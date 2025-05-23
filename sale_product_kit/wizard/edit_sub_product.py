# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, api, fields, models


class EditSubProduct(models.TransientModel):
    _name = 'edit.sub.product'

    @api.model
    def default_get(self, fields):
        defaults = super().default_get(fields)
        sale_order_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
        line_ids = []
        for sub_product in sale_order_line.product_id.sub_product_ids:
            quantity = 0
            price_unit = sub_product.lst_price
            if sub_order_line := sale_order_line.sub_line_ids.filtered(lambda line: line.product_id.id == sub_product.id):
                quantity = sub_order_line.product_uom_qty
                price_unit = sub_order_line.price_sub_product
            line_ids.append(Command.create({
                'product_id': sub_product.id,
                'quantity': quantity,
                'price_unit': price_unit,
            }))
        defaults.update({
            'sale_order_line_id': sale_order_line.id,
            'line_ids': line_ids,
        })
        return defaults

    sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', required=True, ondelete="cascade")
    product_id = fields.Many2one(related='sale_order_line_id.product_id', required=True, ondelete="cascade")
    line_ids = fields.One2many(comodel_name='edit.sub.product.line', inverse_name='edit_sub_product_id', string="Sub Products", required=True)

    def action_confirm(self):
        self.ensure_one()
        commands = []
        for line in self.line_ids:
            if sub_line := self.sale_order_line_id.sub_line_ids.filtered(lambda order_line: order_line.product_id.id == line.product_id.id):
                if line.quantity == 0:
                    commands.append(Command.unlink(sub_line.id))
                elif line.quantity != sub_line.product_uom_qty or line.price_unit != sub_line.price_sub_product:
                    commands.append(Command.update(sub_line.id, {
                        'product_uom_qty': line.quantity,
                        'price_unit': 0.0,
                        'price_sub_product': line.price_unit,
                    }))
            elif line.quantity > 0:
                commands.append(Command.create({
                    'price_sub_product': line.price_unit,
                    'price_unit': 0.0,
                    'product_uom_qty': line.quantity,
                    'product_id': line.product_id.id,
                    'order_id': self.sale_order_line_id.order_id.id,
                    'kit_line_id': self.sale_order_line_id.id,
                }))
        price_unit = sum(line.quantity * line.price_unit for line in self.line_ids)
        self.sale_order_line_id.update({
            'price_unit': price_unit,
            'sub_line_ids': commands,
        })
        return True
