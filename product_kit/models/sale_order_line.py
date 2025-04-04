from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(related="product_template_id.is_kit", store=True)
    from_wizard = fields.Boolean(string="Created from Wizard", default=False)

    def action_open_kit_wizard(self):
        """Opens the wizard with Sale Order ID in context"""
        return {
            "name": "Kit Products",
            "type": "ir.actions.act_window",
            "res_model": "kit.products.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_sale_order_id": self.order_id.id,
                "default_product_template_id": self.product_template_id.id,
            }
        }

    def unlink(self):
        """Delete only the related wizard-generated sale order lines when a main product line is deleted."""
        main_product_lines = self.filtered(lambda line: not line.from_wizard)

        for main_line in main_product_lines:
            kit_lines = self.search([
                ("order_id", "=", main_line.order_id.id),
                ("from_wizard", "=", True),
                ("product_id", "in", main_line.product_id.kit_product_ids.ids),
            ])
            kit_lines.unlink()

        return super().unlink()
