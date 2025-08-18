from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super().action_confirm()
        for production in self.mrp_production_ids:
            selected_order_line = self.order_line.filtered(lambda line: line.product_id == production.product_id and line.product_uom_qty == production.product_qty)
            for stock_line in production.move_raw_ids.filtered(lambda component: component.modular_type_id):
                stock_line.product_uom_qty *= stock_line.modular_type_id.multiplier if selected_order_line.is_modular_type_set else 0
        return res
