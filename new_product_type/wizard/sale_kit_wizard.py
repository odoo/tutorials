from odoo import models, fields, api
from odoo.fields import Command


class SaleKitWizard(models.TransientModel):
    _name = 'sale.kit.wizard'
    _description = 'Sale Kit Sub Products Wizard'

    order_line_id = fields.Many2one('sale.order.line', string='Order Line', required=True)
    product_id = fields.Many2one('product.template', string='Product')
    wizard_line_ids = fields.One2many(
        'sale.kit.wizard.line',
        inverse_name='wizard_id',
        string='Sub Products',
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')

        if active_model != 'sale.order.line' or not active_id:
            return res

        sale_line = self.env['sale.order.line'].browse(active_id)
        if not sale_line.product_id:
            return res

        product = sale_line.product_id
        kit_sub_product = []

        for sub in product.product_tmpl_id.sub_product_ids:
            existing_line = sale_line.order_id.order_line.filtered(
                lambda line: line.product_id == sub
                and line.kit_main_line_id == sale_line
            )
            kit_sub_product.append(
                Command.create({
                    'product_id': sub.id,
                    'quantity': existing_line.product_uom_qty
                        if existing_line else 1.0,
                    'price': existing_line.kit_unit_price
                        if existing_line else sub.lst_price,
                })
            )

        res.update({
            'product_id': product.product_tmpl_id.id,
            'order_line_id': sale_line.id,
            'wizard_line_ids': kit_sub_product,
        })
        return res

    def action_confirm_kit(self):
        self.ensure_one()

        parent_line = self.order_line_id
        order = parent_line.order_id
        total_price = parent_line.product_id.lst_price

        for wiz_line in self.wizard_line_ids:
            existing_line = order.order_line.filtered(
                lambda line: line.product_id == wiz_line.product_id
                and line.kit_main_line_id == parent_line
            )

            values = {
                'product_uom_qty': wiz_line.quantity,
                'price_unit': 0.0,
                'kit_unit_price': wiz_line.price,
                'sequence': parent_line.sequence,
            }

            if existing_line:
                existing_line.write(values)
            else:
                self.env['sale.order.line'].create({
                    **values,
                    'name': wiz_line.product_id.name,
                    'order_id': order.id,
                    'product_id': wiz_line.product_id.id,
                    'is_kit_sub_line': True,
                    'kit_main_line_id': parent_line.id,
                })
            total_price += wiz_line.price * wiz_line.quantity
        parent_line.write({'price_unit': total_price})
        return {'type': 'ir.actions.act_window_close'}
