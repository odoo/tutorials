from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(related="product_template_id.is_kit")
    parent_line_id = fields.Many2one("sale.order.line", ondelete="cascade")

    @api.ondelete(at_uninstall=False)
    def _ondelete_sale_order_line(self):
        if not self.parent_line_id:
            for line in self:
                sub_product_lines = self.env["sale.order.line"].search(
                    [("parent_line_id", "=", line.id)]
                )
                sub_product_lines.with_context(allow_child_unlink=True).unlink()
        else:
            if not self.env.context.get("allow_child_unlink"):
                raise UserError(
                    "You cannot delete a child line directly. Please delete the parent line instead."
                )

    def write(self, vals):
        if "product_uom_qty" in vals and not self.parent_line_id:
            for line in self:
                sub_product_lines = self.env["sale.order.line"].search(
                    [("parent_line_id", "=", line.id)]
                )
                old_qty = line.product_uom_qty
                for sub_line in sub_product_lines:
                    if sub_line:
                        if old_qty != 0:
                            qty = sub_line.product_uom_qty / old_qty
                            new_qty = vals["product_uom_qty"] * qty
                            sub_line.update({"product_uom_qty": new_qty})
                        else:
                            new_qty = vals["product_uom_qty"] * sub_line.product_uom_qty
                            sub_line.update({"product_uom_qty": new_qty})
        return super().write(vals)

    def action_subproduct(self):
        return {
            "type": "ir.actions.act_window",
            "name": f"Product: {self.product_id.name}",
            "res_model": "sub.product.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_sale_order_line_id": self.id},
        }
