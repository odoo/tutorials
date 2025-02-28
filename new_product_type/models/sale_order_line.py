from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_kit_product = fields.Boolean(related='product_id.is_kit')

    def action_list_subproducts(self):
        product_list = (
            [
                [rec.product_id.id, rec.product_uom_qty, rec.product_id.list_price, rec.id]
                for rec in self.linked_line_ids
            ]
            if self.linked_line_ids
            else [
                [rec.id, 1, rec.list_price, 0]
                for rec in self.product_id.sub_products_ids
            ]
        )

        return {
            "type": "ir.actions.act_window",
            "target": "new",
            "res_model": "",
            "view_mode": "form",
            "context": {
                "pname": self.product_id.name,
                "sale_order_id": self.order_id.id,
                "product_ids": product_list,
            },
        }
