from odoo import fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(related="product_template_id.is_kit", store=True, readonly=True)
    kit_product_ids = fields.Many2many("product.product", related="product_template_id.kit_product_ids", string="Kit Products")
    is_sub_product = fields.Boolean(default=False, store=True)

    def action_open_add_kit_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sub Product',
            'res_model': 'sub.product.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_sale_order_line_id': self.id},  
        }

    def unlink(self):
        for line in self:
            if not line.is_sub_product:
                sale_order_line_id=line.id
                sub_lines = self.search([
                    ('product_id', '=', line.product_id.id),
                    ('is_sub_product', '=', True),
                    ('linked_line_id', '=', sale_order_line_id)
                ])
                if sub_lines:
                    sub_lines.unlink()
        return super(SaleOrderLine, self).unlink()
