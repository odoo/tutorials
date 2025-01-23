from odoo import api, Command, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_open_warranty_wizard(self):
        return {
            "name": "Add Warranty",
            "type": "ir.actions.act_window",
            "res_model": "product.warranty.wizard",
            "view_mode": "form",
            "target": "new",
        }

    @api.onchange("order_line")
    def _onchange_order_line(self):
        super()._onchange_order_line()
        deleted_product_template_ids = []
        for line in self.order_line:
            # Find each products that is not in Sale Order currently
            if (
                line.linked_line_id.id
                and line.linked_line_id.id not in self.order_line.ids
            ):
                deleted_product_template_ids.append(line.linked_line_id.id)

        linked_line_ids_to_delete = self.order_line.search(
            [("linked_line_id", "in", deleted_product_template_ids)]
        )
        self.order_line = [
            Command.unlink(linked_line_id)
            for linked_line_id in linked_line_ids_to_delete.ids
        ]
