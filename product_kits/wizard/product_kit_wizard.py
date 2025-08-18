from odoo import Command, api, fields, models


class ProductKitWizard(models.TransientModel):
    _name = 'product.kit.wizard'
    _description = 'Product Kit Wizard to configure sub-products'

    product_name = fields.Char(readonly=True)
    sale_order_line_id = fields.Many2one(
        comodel_name='sale.order.line', string='Sale Order Line', required=True
    )
    wizard_line_ids = fields.One2many(
        comodel_name='product.kit.wizard.line',
        inverse_name='wizard_id',
        string='Product Kit Wizard Lines',
        required=True,
    )

    @api.depends('sale_order_line_id')
    def _compute_product_name(self):
        """
        Compute the product name based on the sale order line.
        """
        for wizard in self:
            if (
                wizard.sale_order_line_id
                and wizard.sale_order_line_id.product_template_id
            ):
                wizard.product_name = wizard.sale_order_line_id.product_template_id.name
            else:
                wizard.product_name = 'UNKNOWN PRODUCT'

    @api.model
    def default_get(self, field_ids):
        """
        Override default_get to set default values for the wizard.
        Populates the wizard with existing values if available.
        If no existing values are found, it initializes the wizard with 0 qty
        """
        result = super().default_get(field_ids)
        if self.env.context.get(
            'active_model'
        ) == 'sale.order.line' and self.env.context.get('active_id'):
            so_line = self.env['sale.order.line'].browse(
                self.env.context.get('active_id')
            )
            existing_sub_lines = self.env['sale.order.line'].search([
                ('parent_kit_line_id', '=', so_line.id)
            ])
            sub_products = so_line.product_id.sub_product_ids

            # Use the existing sub-product lines if available
            # Otherwise, create new lines with 0 qty and default price
            wizard_lines = []
            for component in sub_products:
                component_line = existing_sub_lines.filtered(
                    lambda x: x.product_id.id == component.id
                )
                if component_line:
                    wizard_lines.append({
                        'product_id': component_line.product_id.id,
                        'quantity': component_line.product_uom_qty,
                        'price': component_line.custom_sub_product_price
                        or component.lst_price,
                    })
                else:
                    wizard_lines.append({
                        'product_id': component.id,
                        'quantity': 0.0,
                        'price': component.lst_price,
                    })

            wiz_lines = self.env['product.kit.wizard.line'].create(wizard_lines)

            result.update({
                'product_name': so_line.product_template_id.name,
                'sale_order_line_id': so_line.id,
                'wizard_line_ids': [Command.set(wiz_lines.ids)],
            })
        return result

    def save_configuration(self):
        self.ensure_one()
        kit_so_line = self.sale_order_line_id
        kit_price = 0
        sub_so_lines = kit_so_line.sub_product_line_ids
        current_sequence = kit_so_line.sequence

        for line in self.wizard_line_ids:
            sub_product_line = sub_so_lines.filtered(
                lambda x: x.product_id.id == line.product_id.id
            )
            kit_price += line.price * line.quantity

            # If the sub-product line already exists, update it
            # Otherwise, create a new one
            if not sub_product_line:
                self.env['sale.order.line'].create({
                    'order_id': kit_so_line.order_id.id,
                    'parent_kit_line_id': kit_so_line.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'price_unit': 0,
                    'custom_sub_product_price': line.price,
                    'sequence': current_sequence,
                })
            else:
                sub_product_line.write({
                    'product_uom_qty': line.quantity,
                    'custom_sub_product_price': line.price,
                    'price_unit': 0,
                })

        kit_so_line.write({'price_unit': kit_price})
        return {'type': 'ir.actions.act_window_close'}
