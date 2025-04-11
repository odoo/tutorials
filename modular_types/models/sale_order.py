from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            for production in order.mrp_production_ids:
                # Find matching order line
                matching_order_lines = order.order_line.filtered(lambda line:
                    line.product_id == production.product_id and
                    line.product_uom_qty == production.product_qty
                )
                if not matching_order_lines:
                    continue
                for matching_line in matching_order_lines:
                    for component in production.move_raw_ids.filtered(lambda comp: comp.modular_type_id):
                        # Look up modular value for that line and modular type
                        modular_value = self.env['sale.order.line.modular.value'].search([
                            ('order_line_id', '=', matching_line.id),
                            ('modular_type_id', '=', component.modular_type_id.id)
                        ], limit=1)
                        component.product_uom_qty *= modular_value.value if modular_value else 0.0
        return res
