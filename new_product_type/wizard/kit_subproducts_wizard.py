from odoo import api, Command, fields, models


class KitSubproductWizard(models.TransientModel):
    _name = 'kit.subproduct.wizard'
    _description = 'Wizard for configuring kit subproducts'

    subproduct_lines_ids = fields.One2many('kit.subproduct.wizard.line', 'kit_configuration_id', default=lambda self: self._default_subproduct_lines())

    def _default_subproduct_lines(self):
        sale_order_line_id = self.env.context.get('active_id')
        if not sale_order_line_id:
            return []
        subproduct_line_ids = self.env['kit.subproduct.wizard.line'].with_context(
            kit_configuration_id=self.id, active_id=sale_order_line_id
        )._prepare_subproduct_lines()
        return [Command.set(subproduct_line_ids.ids)]

    def action_apply_configuration(self):
        sale_order_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
        if not sale_order_line:
            return

        sale_order = sale_order_line.order_id
        total_subproduct_price = 0
        configured_lines = self.subproduct_lines_ids

        existing_subproduct_lines = self.env['sale.order.line'].search([
            ('parent_line_id', '=', sale_order_line.id),
            ('order_id', '=', sale_order.id)
        ])
        existing_subproduct_map = {line.product_id.id: line for line in existing_subproduct_lines}

        new_subproduct_values = []
        updated_subproduct_values = []

        for configured_line in configured_lines:
            if configured_line.product_id.id in existing_subproduct_map:
                existing_line = existing_subproduct_map[configured_line.product_id.id]
                updated_subproduct_values.append((1, existing_line.id, {
                    'product_uom_qty': configured_line.quantity,
                    'price_unit': 0,
                }))
                total_subproduct_price += configured_line.quantity * configured_line.unit_price
            else:
                new_subproduct_values.append({
                    'order_id': sale_order.id,
                    'name': configured_line.product_id.name,
                    'product_id': configured_line.product_id.id,
                    'product_template_id': configured_line.product_id.product_tmpl_id.id,
                    'product_uom_qty': configured_line.quantity,
                    'price_unit': 0,
                    'parent_line_id': sale_order_line.id,
                    'is_subproduct': True,
                })
                total_subproduct_price += configured_line.quantity * configured_line.unit_price

        if new_subproduct_values:
            self.env['sale.order.line'].create(new_subproduct_values)
        if updated_subproduct_values:
            sale_order.write({'order_line': updated_subproduct_values})

        sale_order_line.price_unit = total_subproduct_price


class KitSubproductWizardLine(models.TransientModel):
    _name = 'kit.subproduct.wizard.line'
    _description = 'Line for Kit Subproduct Configuration'

    kit_configuration_id = fields.Many2one('kit.subproduct.wizard')
    product_id = fields.Many2one(comodel_name='product.product', required=True)
    unit_price = fields.Float(string='Unit Price')
    quantity = fields.Float(string='Quantity', default=1.0)

    def _prepare_subproduct_lines(self):
        sale_order_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
        product = sale_order_line.product_id.product_tmpl_id
        existing_wizard_lines = self.search([('kit_configuration_id', '=', self.env.context.get("kit_configuration_id", False))])

        if existing_wizard_lines:
            return existing_wizard_lines

        existing_sale_subproduct_lines = self.env['sale.order.line'].search([
            ('parent_line_id', '=', sale_order_line.id),
            ('order_id', '=', sale_order_line.order_id.id)
        ])
        existing_subproduct_map = {line.product_id.id: line for line in existing_sale_subproduct_lines}

        subproduct_line_values = []
        for sub_product in product.sub_products_ids:
            if sub_product.id in existing_subproduct_map:
                existing_line = existing_subproduct_map[sub_product.id]
                quantity = existing_line.product_uom_qty
                unit_price = sub_product.list_price
            else:
                quantity = 1.0
                unit_price = sub_product.list_price

            subproduct_line_values.append({
                'kit_configuration_id': self.env.context.get("kit_configuration_id", False),
                'product_id': sub_product.id,
                'unit_price': unit_price,
                'quantity': quantity,
            })

        return self.create(subproduct_line_values)
