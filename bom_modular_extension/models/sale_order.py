from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super().action_confirm()

        for production in self.mrp_production_ids:
            selected_order_line = self.order_line.filtered(
                lambda line: line.product_id == production.product_id
                and line.product_uom_qty == production.product_qty
            )

            for stock_line in production.move_raw_ids.filtered(
                lambda move: move.modular_type_id
            ):
                modular_value = (
                    selected_order_line.mapped("modular_type_value_ids")
                    .filtered(lambda m: m.modular_type_id == stock_line.modular_type_id)
                    .value
                )

                stock_line.product_uom_qty *= modular_value or 0.0

        return res
