from odoo import api, fields, models


class KitSubproductsWizard(models.TransientModel):
    _name = 'kit.subproducts.wizard'
    _description = 'Wizard for managing kit subproducts'

    def _get_default(self):
        sale_order_line_id = self.env.context.get('active_id')
        if not sale_order_line_id:
            return []
        return self.env['kit.subproducts.wizard.line']._create_or_update_lines(sale_order_line_id)

    sub_line_ids = fields.One2many(
        'kit.subproducts.wizard.line', 'wizard_id', 
        default=_get_default
    )

    def action_confirm(self):
        sale_order_line_id = self.env.context.get('active_id')
        sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)
        if not sale_order_line:
            return

        # Use a single create for all new lines
        new_lines_vals = []
        total = 0
        for line in self.sub_line_ids:
            existing_line = sale_order_line.order_id.order_line.filtered(
                lambda l: l.parent_line_id == sale_order_line and l.product_id == line.product_id
            )
            if existing_line:
                existing_line.product_uom_qty = line.product_uom_qty
            else:
                new_lines_vals.append({
                    'order_id': sale_order_line.order_id.id,
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_template_id': line.product_id.product_tmpl_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'price_unit': 0,
                    'parent_line_id': sale_order_line_id,
                    'is_subproduct': True,
                })
            total += line.product_uom_qty * line.price_unit

        if new_lines_vals:
            self.env['sale.order.line'].create(new_lines_vals)

        sale_order_line.price_unit = total
        return {'type': 'ir.actions.act_window_close'}


class KitSubproductsWizardLine(models.TransientModel):
    _name = 'kit.subproducts.wizard.line'
    _description = 'Wizard Line for Kit Subproducts'

    wizard_id = fields.Many2one('kit.subproducts.wizard')
    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(string='Unit Price')
    product_uom_qty = fields.Float(string='Quantity', default=1.0)

    @api.model
    def _create_or_update_lines(self, sale_order_line_id):
        sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)
        product_tmpl_id = sale_order_line.product_id.product_tmpl_id
        existing_lines = self.env['kit.subproducts.wizard.line'].search([
            ('wizard_id', '=', self.env.context.get('wizard_id'))
        ])
        if existing_lines:
            return [(6, 0, existing_lines.ids)]

        # Use a single create for all new lines
        vals_list = []
        for sub_product in product_tmpl_id.sub_products_ids:
            existing_sale_line = sale_order_line.order_id.order_line.filtered(
                lambda l: l.parent_line_id == sale_order_line and l.product_id == sub_product
            )
            qty = existing_sale_line.product_uom_qty if existing_sale_line else 1.0
            vals_list.append({
                'wizard_id': self.env.context.get('wizard_id'),
                'product_id': sub_product.id,
                'price_unit': sub_product.list_price,
                'product_uom_qty': qty,
            })
        return [(0, 0, vals) for vals in vals_list]
