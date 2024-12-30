from odoo import models, fields, api, Command


class SaleOrder(models.Model):
    _inherit = "sale.order"

    has_warranty = fields.Boolean(compute="_compute_has_warranty", store=True)

    @api.depends("order_line.product_id.warranty", "order_line.warranty_line_ids")
    def _compute_has_warranty(self):
        for order in self:
            order.has_warranty = any(
                line.product_id.warranty and not line.warranty_line_ids
                for line in order.order_line
            )

    def open_warranty_wizard(self):
        order_lines_with_warranty = self.order_line.filtered(
            lambda line: line.product_id.warranty and not line.warranty_line_ids
        )

        wizard = self.env["product.warranty.wizard"].create(
            {
                "product_ids": [
                    Command.create({"product_id": line.product_id.id, "main_order_line": line.id})
                    for line in order_lines_with_warranty
                ]
            }
        )

        return {
            "name": "Warranty Wizard",
            "view_mode": "form",
            "res_model": "product.warranty.wizard",
            "res_id": wizard.id,
            "type": "ir.actions.act_window",
            "target": "new",
        }
