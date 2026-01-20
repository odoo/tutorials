from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    new_picking_ids = fields.Many2many(
        "stock.picking",
        "stock_picking_sale_order_rel",
        "sale_id", 
        "picking_id", 
        string="Related Pickings",
        copy=False, 
        help="This field links pickings related to the sale order."
    )

    @api.depends("picking_ids","new_picking_ids")
    def _compute_picking_ids(self):
        for order in self:
            order.delivery_count = len(set(order.picking_ids.ids + order.new_picking_ids.ids))

    def action_view_delivery(self):
        all_pickings = self.picking_ids + self.new_picking_ids
        return self._get_action_view_picking(all_pickings)
                