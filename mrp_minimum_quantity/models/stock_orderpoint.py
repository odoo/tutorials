# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, models
from odoo.exceptions import UserError


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    def action_replenish(self, force_to_max=False):
        is_mrp_admin = self.env.user.has_group("mrp.group_mrp_manager")
        errors = []
        for orderpoint in self:
            if not orderpoint.rule_ids.filtered(lambda r: r.action == "manufacture"):
                continue
            bom = self.env["mrp.bom"]._bom_find(self.product_id).get(self.product_id)
            if not bom:
                continue
            if orderpoint.qty_to_order < bom.product_min_qty:
                if orderpoint.trigger == "manual":
                    message = _(
                        f"The quantity to order ({orderpoint.qty_to_order}) is less than the minimum required ({bom.product_min_qty}) for product '{orderpoint.product_id.display_name}'."
                    )
                    if is_mrp_admin:
                        errors.append(message)
                    else:
                        raise UserError(message)
                else:
                    orderpoint.qty_to_order = bom.product_min_qty
        notification = super().action_replenish(force_to_max)
        if errors:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Warning"),
                    "message": "\n".join(errors),
                    "sticky": False,
                    "type": "warning"
                }
            }
        return notification
