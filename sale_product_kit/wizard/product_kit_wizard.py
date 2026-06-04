from odoo import api, fields, models


class ProductKitWizard(models.TransientModel):
    _name = "product.kit.wizard"
    _description = "Product Kit Wizard"

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        order_line = self.env['sale.order.line'].browse(
            self.env.context.get('active_order_line_id')
        )
        if order_line.child_kit_line_ids:
            wizard_lines = [
                (0, 0, {
                    'sub_product_id': line.product_id.id,
                    'quantity': line.product_uom_qty,
                    'price': line.kit_component_price,
                })
                for line in order_line.child_kit_line_ids
            ]
        else:
            wizard_lines = [
                (0, 0, {
                    'sub_product_id': sp.id,
                    'quantity': 1,
                    'price': sp.lst_price,
                })
                for sp in order_line.product_template_id.sub_product_ids
            ]
        res.update({
            'product_id': order_line.product_id.id,
            'wizard_line_ids': wizard_lines,
        })
        return res

    product_id = fields.Many2one('product.product')
    wizard_line_ids = fields.One2many("product.kit.wizard.line", "wizard_id")

    def add_sub_product_value(self):
        parent_line = self.env['sale.order.line'].browse(
            self.env.context.get('active_order_line_id')
        )
        total_price = 0
        existing_children = {
            line.product_id.id: line
            for line in parent_line.child_kit_line_ids
        }
        create_vals = []
        for wizard_line in self.wizard_line_ids:
            total_price = total_price + (wizard_line.price * wizard_line.quantity)
            product_id = wizard_line.sub_product_id.id
            existing_child = existing_children.get(product_id)
            if existing_child:
                existing_child.write({
                    'product_uom_qty': wizard_line.quantity,
                    'price_unit': 0,
                    'kit_component_price': wizard_line.price,
                })
            else:
                create_vals.append({
                    'order_id': parent_line.order_id.id,
                    'product_id': product_id,
                    'product_uom_qty': wizard_line.quantity,
                    'kit_component_price': wizard_line.price,
                    'price_unit': 0,
                    'parent_kit_line_id': parent_line.id,
                    'is_kit_child': True,
                })
        if create_vals:
            self.env['sale.order.line'].create(create_vals)
        parent_line.price_unit = total_price
        return True


class ProductKitWizardLine(models.TransientModel):
    _name = 'product.kit.wizard.line'
    _description = 'Product Kit Wizard Lines'

    wizard_id = fields.Many2one('product.kit.wizard')
    sub_product_id = fields.Many2one('product.product')
    quantity = fields.Integer(default=1)
    price = fields.Float()
