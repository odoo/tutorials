from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("picking_ids")
    def _compute_picking_ids(self):
        for order in self:
            extra_pickings = self.env["stock.picking"].search([("sale_ids", "in", order.id)])
            order.delivery_count = len(order.picking_ids | extra_pickings)

    def action_view_delivery(self):
        extra_pickings = self.env["stock.picking"].search([("sale_ids", "in", self.id)])
        return self._get_action_view_picking(self.picking_ids | extra_pickings)
