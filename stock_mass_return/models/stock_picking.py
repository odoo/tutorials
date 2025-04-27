from odoo import api, fields, models, _

class StockPicking(models.Model):
    _inherit = "stock.picking"

    sale_ids = fields.Many2many(
        "sale.order",
        "stock_picking_sale_order_rel", 
        "picking_id",
        "sale_id",  
        string="Sale Orders",
        copy=False, 
        help="This field links multiple sale order."
    )

    new_return_ids = fields.Many2many(
        "stock.picking", 
        "stock_picking_new_return_rel",
        "picking_id",
        "return_id",
        string="Return of",
        copy=False,
        readonly=True,
        help="This field links multiple return pickings to a single original picking."
    )

    new_picking_ids = fields.Many2many(
        "stock.picking", 
        "stock_picking_new_return_rel",
        "return_id",
        "picking_id",
        string="Return of Multiple Pickings",
        copy=False,
        readonly=True,
        help="This field links multiple original pickings to a single return picking."
    )

    @api.depends("return_ids", "new_return_ids")
    def _compute_return_count(self):
        for picking in self:
            picking.return_count = len(set(picking.return_ids.ids + picking.new_return_ids.ids))

    def action_see_returns(self):
        self.ensure_one()
        returns = self.return_ids | self.new_return_ids
        if len(returns) == 1:
            return {
                "type": "ir.actions.act_window",
                "res_model": "stock.picking",
                "views": [[False, "form"]],
                "res_id": returns.id
            }
        return {
            "name": _("Returns"),
            "type": "ir.actions.act_window",
            "res_model": "stock.picking",
            "views": [[False, "list"], [False, "form"]],
            "domain": [("id", "in", returns.ids)],
        }

    def _get_next_transfers(self):
        next_pickings = super()._get_next_transfers()
        return next_pickings.filtered(lambda p: p not in self.new_return_ids)
