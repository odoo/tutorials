from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super().action_confirm()
        for production in self.mrp_production_ids:
            matching_order_line = self.order_line.filtered(lambda line: 
                line.product_id == production.product_id and 
                line.product_uom_qty == production.product_qty
            )
            for component in production.move_raw_ids.filtered(lambda comp: comp.modular_type_id):
                component.product_uom_qty *= component.modular_type_id.qty_multiplier if matching_order_line.is_modular_type_set else 0
        return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    has_available_modular_type = fields.Boolean(
        string="Has Available Modular Type",
        compute='_compute_has_available_modular_type',
        store=True
    )
    is_modular_type_set = fields.Boolean(string="Is Modular Type Set")

    @api.depends('product_id')
    def _compute_has_available_modular_type(self):
        for line in self:
            line.has_available_modular_type = bool(
                line.product_id.product_tmpl_id.modular_type_ids
            ) if line.product_id else False
