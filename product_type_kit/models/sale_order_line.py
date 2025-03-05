from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_is_kit = fields.Boolean(related='product_template_id.is_kit', string="Is Kit")
    product_state = fields.Selection(related='order_id.state', string="Product Status")

    def action_open_kit_products(self):
        """Opens a wizard showing the sub-products of the selected kit product."""
        self.ensure_one()
        if not self.product_template_id or not self.product_template_id.is_kit:
            return

        return {
            'type': 'ir.actions.act_window',
            'name': f'Kit Product: {self.product_id.name}',
            'res_model': 'product.type.kit.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_product_id': self.product_template_id.id},
        }
