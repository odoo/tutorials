from odoo import _, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_kit = fields.Boolean(related="product_template_id.is_kit")
    is_kit_component = fields.Boolean(string="Is Subproduct")
    kit_parent_line_id = fields.Many2one('sale.order.line', string="Kit Parent Line", ondelete="cascade")
    kit_unit_cost = fields.Float(string="Unit Price (Wizard)", default=0.0)

    def action_open_kit_wizard(self):
        return {
            'name': 'Kit Components',
            'type': 'ir.actions.act_window',
            'res_model': 'kit.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                "active_id": self.order_id.id,
                'default_product_id': self.product_id.id,
                'default_sale_order_line_id': self.id,
            }
        }

    def unlink(self):
        # Identify sub-product lines
        sub_products = self.filtered(lambda line: line.is_kit_component)

        if sub_products and not self.env.context.get('allow_sub_product_deletion'):
            if self == sub_products:
                raise models.UserError(_("You cannot delete kit sub-products directly. Delete the main kit line instead."))
            return (self - sub_products).unlink()

        child_lines = self.env['sale.order.line'].search([
            ('kit_parent_line_id', 'in', self.ids)
        ])

        if child_lines:
            child_lines.with_context(allow_sub_product_deletion=True).unlink()

        return super().unlink()
