from odoo import api, Command, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    has_warranty = fields.Boolean(compute="_compute_has_warranty")

    @api.depends(
        "order_line.product_id.is_warranty_available", "order_line.warranty_linked_ids"
    )
    def _compute_has_warranty(self):
        for order in self:
            order.has_warranty = any(
                line.product_id.is_warranty_available and not line.warranty_linked_ids
                for line in order.order_line
            )

    def action_open_warranty_wizard(self):
        active_product_ids = [
            line
            for line in self.order_line
            if line.product_id.is_warranty_available and not line.warranty_linked_ids
        ]

        warranty_wizard = self.env["add.warranty"].create(
            {
                "warranty_lines_ids": [
                    Command.create(
                        {"product_id": line.product_id.id, "order_line_id": line.id}
                    )
                    for line in active_product_ids
                ]
            }
        )

        return {
            "type": "ir.actions.act_window",
            "name": "Add Warranty",
            "res_model": "add.warranty",
            "res_id": warranty_wizard.id,
            "view_mode": "form",
            "target": "new",
        }
