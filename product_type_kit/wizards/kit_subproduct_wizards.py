# wizards/kit_sub_product_wizard.py
from odoo import api, fields, models


class KitSubProductWizard(models.TransientModel):
    _name = 'kit.sub.product.wizard'
    _description = 'Kit Sub Products Wizard'

    order_line_id = fields.Many2one('sale.order.line', required=True)
    sub_product_lines = fields.One2many('kit.sub.product.line', 'wizard_id')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        line = self.env['sale.order.line'].browse(self.env.context['default_order_line_id'])
        previous_sub_lines = self.env['sale.order.line'].search([
            ('kit_parent_line_id', '=', line.id)
        ])
        sub_lines = []
        for sub_product in line.product_id.sub_product_ids:
            prev_line = previous_sub_lines.filtered(lambda l: l.product_id == sub_product)
            sub_lines.append((0, 0, {
                'product_id': sub_product.id,
                'quantity': prev_line.product_uom_qty if prev_line else 1.0,
                'price_unit': prev_line.price_unit if prev_line else sub_product.lst_price,
            }))
        res['sub_product_lines'] = sub_lines
        return res

    def action_confirm(self):
        SaleOrderLine = self.env['sale.order.line']
        # Remove existing kit sub lines
        existing_lines = SaleOrderLine.search([('kit_parent_line_id', '=', self.order_line_id.id)])
        existing_lines.unlink()

        for sub_line in self.sub_product_lines:
            SaleOrderLine.create({
                'order_id': self.order_line_id.order_id.id,
                'product_id': sub_line.product_id.id,
                'product_uom_qty': sub_line.quantity,
                'price_unit': 0.0,
                'kit_parent_line_id': self.order_line_id.id,
            })

        total_price = sum(l.quantity * l.price_unit for l in self.sub_product_lines)
        self.order_line_id.price_unit = total_price
