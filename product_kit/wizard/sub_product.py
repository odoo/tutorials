from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SubProductWizard(models.TransientModel):
    _name = 'sub.product.wizard'
    _description = 'Sub Product Wizard'

    sale_order_line_id = fields.Many2one('sale.order.line', string="Sale Order Line", required=True)
    product_id = fields.Many2one('product.product', string="Main Product", required=True)
    sub_product_lines = fields.One2many('sub.product.line.wizard', 'wizard_id', string="Sub Products")

    @api.model
    def default_get(self, fields):
        defaults = super().default_get(fields)
        sale_order_line_id = self.env.context.get('default_sale_order_line_id')
        sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)
        if not sale_order_line:
            return defaults
        product_template = sale_order_line.product_id.product_tmpl_id
        line_data = []
        # Check if there's existing wizard for the same sale order line
        existing_wizard = self.search([('sale_order_line_id', '=', sale_order_line_id)])
        if existing_wizard:
            for line in existing_wizard.sub_product_lines:
                line_data.append((4, line.id))
        else:
            # Fetch sub-products from product template's sub_product_ids
            for sub_product in product_template.sub_product_ids:
                line_data.append((0, 0, {
                    'product_id': sub_product.id,
                    'quantity': 1,
                    'price_unit': sub_product.lst_price,
                }))
        defaults.update({
            'sale_order_line_id': sale_order_line_id,
            'product_id': sale_order_line.product_id.id,
            'sub_product_lines': line_data,
        })
        return defaults

    def confirm_action(self):
        self.ensure_one()
        if not any(self.sub_product_lines.mapped('quantity')):
            raise UserError(_("You must select at least 1 sub-product to proceed."))
        sale_order = self.sale_order_line_id.order_id
        main_product_line = self.sale_order_line_id
        # Get existing sub-product lines for this main product
        existing_sub_lines = {}
        filtered_lines = sale_order.order_line.filtered(
            lambda l: l.parent_line_id == main_product_line
        )
        for line in filtered_lines:
            existing_sub_lines[line.product_id.id] = line
        total_price = 0.0
        for wizard_line in self.sub_product_lines:
            sub_product_id = wizard_line.product_id.id
            if sub_product_id in existing_sub_lines:
                existing_line = existing_sub_lines[sub_product_id]
                existing_line.write({
                    'product_uom_qty': wizard_line.quantity,
                    'price_unit': 0.0,
                    'price_subtotal': 0.0,
                })
            else:
                sequence = main_product_line.sequence
                new_line = self.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'product_id': sub_product_id,
                    'product_uom_qty': wizard_line.quantity,
                    'price_unit': 0.0,
                    'price_subtotal': 0.0,
                    'parent_line_id': main_product_line.id,
                    'sequence': sequence + 1,
                })
                existing_sub_lines[sub_product_id] = new_line
            total_price += wizard_line.quantity * wizard_line.price_unit
        # Update the main product's price
        main_product_line.update({
            'price_unit': total_price,
            'price_subtotal': total_price,
        })
        return {'type': 'ir.actions.act_window_close'}

class SubProductLineWizard(models.TransientModel):
    _name = 'sub.product.line.wizard'
    _description = 'Wizard Sub-Product Line'

    wizard_id = fields.Many2one(comodel_name='sub.product.wizard', string="Wizard", ondelete='cascade', required=True)
    product_id = fields.Many2one(comodel_name='product.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", default=1.0, required=True)
    price_unit = fields.Float(string="Price", required=True)
