from odoo import Command, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def add_warranty(self):
        order_lines_with_warranty = self.order_line.filtered(
            lambda line: line.product_id.is_warranty_available
            and not line.warranty_line_ids
        )
        wizard = self.env["add.warranty.wizard"].create(
            {
                "product_ids": [
                    Command.create(
                        {"product_id": line.product_id.id, "main_order_line": line.id}
                    )
                    for line in order_lines_with_warranty
                ]
            }
        )
        return {
            "name": "Warranty Wizard",
            "view_mode": "form",
            "res_model": "add.warranty.wizard",
            "res_id": wizard.id,
            "type": "ir.actions.act_window",
            "target": "new",
        }
