from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # linked_line_id
    # linked_line_ids
    is_kit = fields.Boolean(related="product_id.is_kit", string="is_kit")

    def action_add_warranty(self):
        product_list = []
        if self.linked_line_ids:
            for record in self.linked_line_ids:
                product_list.append(
                    [
                        record.product_id.id,
                        record.product_uom_qty,
                        record.product_id.list_price,
                        record.id,
                    ]
                )
        else:
            for record in self.product_id.kit_product_ids:
                product_list.append([record.id, 1, record.list_price, 0])

        return {
            "type": "ir.actions.act_window",
            "target": "new",
            "res_model": "product.add.product",
            "view_mode": "form",
            "context": {
                "pname": self.product_id.name,
                "sale_order_id": self.order_id.id,
                "product_ids": product_list,
            },
        }
