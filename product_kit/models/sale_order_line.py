from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    isKit = fields.Boolean(related="product_template_id.isKit", store=True)
    is_subProduct = fields.Boolean(string="Created from Wizard", default=False)
    last_updated_price = fields.Float("Kit Price", help="Custom price stored for use in kit wizard")

    def action_open_kit_wizard(self):
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
        """When main product line is deleted, all the related wizard-generated sale order lines are deleted."""
        main_product_line = self.filtered(lambda line: not line.is_subProduct)

        for sub_product_lines in main_product_line:
            kit_lines = self.search([
                ("order_id", "=", sub_product_lines.order_id.id),
                ("is_subProduct", "=", True),
                ("product_id", "in", sub_product_lines.product_id.subProduct_ids.ids),
            ])
            kit_lines.unlink()

        return super().unlink()
