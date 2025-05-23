# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, Command, fields, models


class SubProductWizard(models.TransientModel):
    _name = 'sub.product.wizard'

    sale_order_line_id = fields.Many2one(comodel_name="sale.order.line")
    product_id = fields.Many2one(comodel_name="product.product", readonly=True, related="sale_order_line_id.product_id")
    sub_product_wizard_line_ids = fields.One2many("sub.product.wizard.line", "sub_product_wizard_id")

    @api.model
    def default_get(self, fields_list):
        defaults = super(SubProductWizard, self).default_get(fields_list)
        current_sale_order_line = self.env['sale.order.line'].search([('id', '=', self.env.context.get('active_id'))])
        defaults.update({
            'sale_order_line_id': current_sale_order_line.id,
            'product_id': current_sale_order_line.product_id.id,
        })
        subproduct_ids = current_sale_order_line.product_id.sub_products.ids
        sub_product_wizard_line_creation_data = []
        for child_line in current_sale_order_line.child_sale_order_line_ids:
            sub_product_wizard_line_creation_data.append(
                Command.create({
                'product_id': child_line.product_id,
                'quantity': child_line.product_uom_qty,
                'sale_order_line_id': child_line.id,
                'price': child_line.actual_price_sub_product
            }))
            subproduct_ids.remove(child_line.product_id.id)

        for i in subproduct_ids:
            sub_product_wizard_line_creation_data.append(
                Command.create({
                'product_id': self.env['product.product'].browse(i),
                'quantity': 0,
                'price': self.env['product.product'].browse(i).lst_price,
            })
            )
        defaults.update({
            'sub_product_wizard_line_ids': sub_product_wizard_line_creation_data,
        })
        return defaults

    def confirm_subproducts(self):
        updated_price = self.sale_order_line_id.product_id.lst_price
        for wizard_line in self.sub_product_wizard_line_ids:
            if wizard_line.sale_order_line_id:
                if wizard_line.quantity:
                    wizard_line.sale_order_line_id.product_uom_qty = wizard_line.quantity
                    wizard_line.sale_order_line_id.price_unit = wizard_line.price
                    updated_price += (wizard_line.quantity * wizard_line.price)
                else:
                    self.sale_order_line_id.child_sale_order_line_ids = [Command.delete(wizard_line.sale_order_line_id.id)]
            else:
                if wizard_line.quantity:
                    self.sale_order_line_id.child_sale_order_line_ids = [(0, 0, {'product_id': wizard_line.product_id.id, 'product_uom_qty': wizard_line.quantity, 'price_unit':0, 'actual_price_sub_product': wizard_line.price, 'order_id':self.sale_order_line_id.order_id.id, 'sequence': self.sale_order_line_id.sequence})]
                    updated_price += (wizard_line.quantity * wizard_line.price)
        self.sale_order_line_id.price_unit = updated_price
