from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super().action_confirm()

        for mrp_production_id in self.mrp_production_ids:
            source_order_line = self.env['sale.order.line'].search([("order_id.name", "=", mrp_production_id.origin), ("product_id", "=", mrp_production_id.product_id.id)])

            for component in mrp_production_id.move_raw_ids:
                if component.modular_type_id:
                    sale_order_modular_values = source_order_line.modular_value_ids.filtered(lambda l: l.modular_type_id.id == component.modular_type_id.id).value
                    component.quantity *= sale_order_modular_values
                    component.product_uom_qty *= sale_order_modular_values

        return res
