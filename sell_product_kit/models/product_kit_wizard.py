# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductKitWizard(models.TransientModel):
    _name = "product.kit.wizard"
    _description = "Product Kit Configuration Wizard"

    product_id = fields.Many2one('product.product', string="Product", readonly=True)
    order_line_id = fields.Many2one('sale.order.line', string="Order Line", readonly=True)
    sub_product_kit = fields.One2many('product.kit.wizard.line', 'wizard_id', string="Sub Products")
    sub_total = fields.Float(string='Sub Total', compute="_compute_sub_total_price")

    @api.model
    def default_get(self, fields_list):
        res = super(ProductKitWizard, self).default_get(fields_list)
        product_id = self.env.context.get('default_product_id')
        order_line_id = self.env.context.get('default_order_line_id')
        if product_id and order_line_id and 'sub_product_kit' in fields_list:
            product = self.env['product.product'].browse(product_id)
            sub_product_wizard = self.env['product.kit.wizard'].search([
                ('order_line_id', '=', order_line_id),
                ('product_id', '=', product_id)],
                order='id desc', limit=1)
            sub_product_list = []
            sub_products = product.sub_product_ids
            if sub_product_wizard.exists():
                sub_product_kit = sub_product_wizard.sub_product_kit
                for sub_product, existing_product in zip(sub_products, sub_product_kit):
                    sub_product_list.append((0, 0, {
                        'product_id': sub_product.id,
                        'sub_product_name': sub_product.product_tmpl_id.name,
                        'quantity': existing_product.quantity,
                        'unit_price': existing_product.unit_price,
                        'subtotal': existing_product.subtotal,
                    }))
            else:
                for sub_product in sub_products:
                    sub_product_list.append((0, 0, {
                        'product_id': sub_product.id,
                        'sub_product_name': sub_product.product_tmpl_id.name,
                        'quantity': 1.0,
                        'unit_price': sub_product.list_price,
                        'subtotal': sub_product.list_price,
                    }))
            res['sub_product_kit'] = sub_product_list
            res['order_line_id'] = order_line_id
        return res

    @api.depends('sub_product_kit.subtotal')
    def _compute_sub_total_price(self):
        for wizard in self:
            wizard.sub_total = sum(line.subtotal for line in wizard.sub_product_kit)

    def action_confirm(self):
        self.ensure_one()
        product_id = self.env.context.get('default_product_id')
        product = self.env['product.product'].browse(product_id)
        if not self.order_line_id:
            return {'type': 'ir.actions.act_window_close'}

        sale_order_id = self.order_line_id.order_id
        sub_product_data = self.env['product.kit.wizard.line'].search([('wizard_id', '=', self.id)], order="id asc")
        changes_made = False
        existing_sub_products = self.env['sale.order.line'].search([
            ('order_id', '=', sale_order_id.id),
            ('parent_line_id', '=', self.order_line_id.id),
            ('is_sub_product', '=', True)
        ])
        for i, sub_product_id in enumerate(product.sub_product_ids):
            wizard_line = sub_product_data[i]
            existing_sub = existing_sub_products.filtered(lambda l: l.product_id.id == sub_product_id.id)
            vals = {
                'order_id': sale_order_id.id,
                'product_id': sub_product_id.id,
                'name': sub_product_id.product_tmpl_id.name,
                'product_uom_qty': wizard_line.quantity,
                'price_unit': 0.0,
                'parent_line_id': self.order_line_id.id,
                'is_sub_product': True,
            }
            if existing_sub:
                if (existing_sub.product_uom_qty != wizard_line.quantity or
                    existing_sub.price_unit != wizard_line.unit_price):
                    existing_sub.write({
                        'product_uom_qty': vals['product_uom_qty'],
                        'price_unit': vals['price_unit']
                    })
                    changes_made = True
            else:
                self.env['sale.order.line'].create(vals)
                changes_made = True

        if changes_made:
            main_product_price = product.product_tmpl_id.list_price
            self.order_line_id.price_unit = main_product_price + self.sub_total

        return {'type': 'ir.actions.act_window_close'}

class ProductKitWizardLine(models.TransientModel):
    _name = "product.kit.wizard.line"
    _description = "Product Kit Wizard Line"

    wizard_id = fields.Many2one('product.kit.wizard', string="Wizard Reference")
    product_id = fields.Many2one('product.product', readonly=True)
    sub_product_name = fields.Char(string="Product Name", readonly=True)
    quantity = fields.Integer(string="Quantity", default=1.0)
    unit_price = fields.Float(string="Unit Price")
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price
