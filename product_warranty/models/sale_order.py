from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order"

    def action_add_warranty(self):
        product_list = []
        for record in self.order_line:
            if record.product_id.is_warranty:
                product_list.append(
                    [record.product_id.id, record.product_uom_qty, record.id]
                )

        return {
            "type": "ir.actions.act_window",
            "target": "new",
            "res_model": "product.add.warranty",
            "view_mode": "form",
            "context": {
                "product_ids": product_list,
            },
        }


# product_idss = self.order_line.filtered(
#             lambda record: record.product_id.is_warranty
#         )
