from odoo import models, fields, api


class InheritedSalesOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(related="product_template_id.is_kit", store=False)
    is_sub_product = fields.Boolean()

    def action_sub_products(self):
        return {
            'name': f'Product: {self.name}',
            'view_mode': 'form',
            'res_model': 'product_kit_type.subproducts',
            'view_id': self.env.ref('product_kit_type.subproducts_view_form').id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.ondelete(at_uninstall=False)
    def unlink_with_sub_product_lines(self):
        for line in self:
            if not line.is_sub_product:
                sale_order_line_id = line.id
                sub_lines = self.search([
                    ('product_id', '=', line.product_id.id),
                    ('is_sub_product', '=', True),
                    ('linked_line_id', '=', sale_order_line_id)
                ])
                if sub_lines:
                    sub_lines.unlink()
