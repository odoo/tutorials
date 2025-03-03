from odoo import fields, models
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(related="product_template_id.is_kit")
    sub_product_ids = fields.Many2many(
        "product.product",
        related="product_template_id.sub_product_ids",
        string="Kit Products",
    )
    is_sub_product = fields.Boolean()

    def action_open_sub_product_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "sub.product.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_sale_order_line_id": self.id,
            },
        }

    def unlink(self):
        for line in self:
            if not line.is_sub_product:
                sub_lines = self.search(
                    [
                        ("is_sub_product", "=", True),
                        ("linked_line_id", "=", line.id),
                    ]
                )
                if sub_lines:
                    sub_lines.with_context(from_wizard=True).unlink()
            elif line.is_sub_product and not self.env.context.get("from_wizard"):
                raise UserError(
                    "You cannot delete the sub product directly. To delete the sub product, you need to delete the main product or remove it through the wizard."
                )
        return super(SaleOrderLine, self).unlink()