from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(related="product_template_id.is_kit")
    parent_line_id = fields.Many2one("sale.order.line", string="Parent Line")

    def action_kit_button(self):
        return {
            "name": "Adjust Sub-Products",
            "type": "ir.actions.act_window",
            "res_model": "sub.product.wizard",
            "view_mode": "form",
            "target": "new",
            "context": { "default_sale_order_line_id": self.id },
        }

    def unlink(self):
        for line in self:
            if not line.parent_line_id:
                child_lines = self.search([("parent_line_id", "=", line.id)]).filtered(
                    lambda l: l not in self
                )
                child_lines.unlink()
                wizards = self.env["sub.product.wizard"].search(
                    [("sale_order_line_id", "=", line.id)]
                )
                wizards.unlink()
        return super(SaleOrderLine, self).unlink()
