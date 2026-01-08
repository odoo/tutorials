from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends("picking_ids")
    def _compute_incoming_picking_count(self):
        for order in self:
            extra_pickings = self.env["stock.picking"].search([("purchase_ids", "in", order.id)])
            order.incoming_picking_count = len(order.picking_ids | extra_pickings)

    def action_view_picking(self):
        extra_pickings = self.env["stock.picking"].search([("purchase_ids", "in", self.id)])
        return self._get_action_view_picking(self.picking_ids | extra_pickings)
