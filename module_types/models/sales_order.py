from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super().action_confirm()
        for production in self.mrp_production_ids:
            selected_order_line = self.order_line.filtered(lambda line: line.product_template_id == production.product_tmpl_id and line.product_uom_qty == production.product_qty)
            for stock_line in production.move_raw_ids.filtered(lambda component: component.module_type_id):
                have_module_types = bool(selected_order_line.product_template_id.module_types)
                stock_line.product_uom_qty *= stock_line.module_type_id.value if have_module_types else 0
        return res
