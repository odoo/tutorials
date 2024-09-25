from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_check_warranty_and_open(self):

        for line in self.order_line:
            if line.product_id and line.product_id.is_warranty_available:
                # Open the warranty wizard
                return {
                    "type": "ir.actions.act_window",
                    "name": "Add Warranty",
                    "res_model": "warranty.wizard",
                    "view_mode": "form",
                    "target": "new",
                    "view_id": self.env.ref("warranty.add_warranty_form_view").id,
                }

        # If no product with a warranty is found, show a warning message
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Warning",
                "message": "No product with an available warranty found in this order.",
                "type": "warning",
                "sticky": False,
            },
        }
