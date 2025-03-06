from odoo import api, fields, models


class ProductTypeKitWizard(models.TransientModel):
    _name = 'product.type.kit.wizard'
    _description = "Wizard for Sub Products of Kit Product"

    sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', string="Sale Order Line")
    sub_product_ids = fields.One2many(
        comodel_name='product.type.kit.wizard.line',
        inverse_name='kit_product_wizard_id',
        string="Sub Products")

    @api.model
    def default_get(self, fields_list):
        """Load existing sub-products if available; otherwise, load defaults."""
        defaults = super().default_get(fields_list)
        sale_order_line_id = self.env.context.get('default_sale_order_line_id')

        if sale_order_line_id:
            sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)
            sub_product_lines = []

            # Check if sub-products already exist in sale order lines
            existing_sub_products = sale_order_line.order_id.order_line.filtered(
                lambda order_line: order_line.kit_parent_line_id == sale_order_line
            )

            if existing_sub_products:
                # Load existing sub-products from sale order lines
                for sub_product in existing_sub_products:
                    sub_product_lines.append((0, 0, {
                        'product_id': sub_product.product_id.id,
                        'quantity': sub_product.product_uom_qty,
                        'price': sub_product.product_template_id.list_price,
                    }))
            else:
                # Load default sub-products from the kit product
                for sub_product in sale_order_line.product_id.sub_products_ids:
                    sub_product_lines.append((0, 0, {
                        'product_id': sub_product.id,
                        'quantity': 1,
                        'price': sub_product.list_price,
                    }))

            defaults['sub_product_ids'] = sub_product_lines
            defaults['sale_order_line_id'] = sale_order_line_id

        return defaults

    def action_confirm(self):
        """Save sub-product changes persistently within sale order lines."""
        self.ensure_one()
        if self.sale_order_line_id:
            sale_order = self.sale_order_line_id.order_id

            self.env['sale.order.line'].search([
                ('kit_parent_line_id', '=', self.sale_order_line_id.id)
            ]).unlink()

            new_order_lines = []
            total_price = 0
            for line in self.sub_product_ids:
                if line.product_id:
                    new_order_lines.append((0, 0, {
                        'order_id': sale_order.id,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.quantity,
                        'price_unit': 0,
                        'kit_parent_line_id': self.sale_order_line_id.id,
                    }))

                    total_price += line.price * line.quantity
                else:
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': 'Warning',
                            'type': 'warning',
                            'message': "This action is not possible.",
                            'next': {'type': 'ir.actions.act_window_close'}
                        }
                    }

            if new_order_lines:
                sale_order.write({'order_line': new_order_lines})

            self.sale_order_line_id.write({ 'price_unit': total_price })
