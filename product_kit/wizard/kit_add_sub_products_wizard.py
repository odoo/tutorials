from odoo import Command, fields, models, _
from odoo.exceptions import UserError


class KitAddSubProductsWizard(models.TransientModel):
    _name = 'kit.add.sub.products.wizard'
    _description = 'this will allow user to add sub products from pop-up'

    sub_product_ids = fields.One2many(comodel_name='kit.sub.product.line.wizard',inverse_name='parent_wizard_id')

    def default_get(self, fields_list):
        default_vals = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        product_kit_obj = self.env['sale.order.line'].browse(active_id)
        sub_products_list = []

        existing_sub_products = self.env['sale.order.line'].search([
            ('parent_kit_id', '=', product_kit_obj.id) ,
            ('order_id', '=', product_kit_obj.order_id.id)
        ])

        if existing_sub_products:
            for sub_product_line in existing_sub_products:
                sub_products_list.append(Command.create({
                    'sub_product_id': sub_product_line.product_id.id,
                    'quantity': sub_product_line.product_uom_qty,
                    'price': sub_product_line.sub_product_price,
                    'order_line_id': sub_product_line.id
                }))
        else:
            for sub_product in product_kit_obj.product_id.sub_products:
                sub_products_list.append(Command.create({
                    'sub_product_id': sub_product.id,
                    'quantity': 1,
                    'price': sub_product.lst_price
                }))

        default_vals.update(sub_product_ids=sub_products_list)

        return default_vals

    def action_confirm_sub_products(self):
        if not self.sub_product_ids:
            raise UserError(_('add atleast one sub-product'))

        active_id = self.env.context.get('active_id')
        product_kit_obj = self.env['sale.order.line'].browse(active_id)
        kit_price = sum(sub_product.quantity * sub_product.price for sub_product in self.sub_product_ids)
        product_kit_obj.write({'price_unit': kit_price})

        for sub_product in self.sub_product_ids:
            if sub_product.order_line_id:
                sub_product.order_line_id.write({
                    'product_uom_qty': sub_product.quantity,
                    'sub_product_price': sub_product.price,
                    'price_unit': 0.0
                })
            else:
                if product_kit_obj.product_id == sub_product.sub_product_id:
                    raise UserError("You can not add product itself as a sub-product")
                self.env['sale.order.line'].create({
                    'order_id': product_kit_obj.order_id.id,
                    'product_id': sub_product.sub_product_id.id,
                    'product_uom_qty': sub_product.quantity,
                    'price_unit': 0.0,
                    'parent_kit_id': product_kit_obj.id,
                    'sub_product_price': sub_product.price
                })

        return True
