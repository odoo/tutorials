# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, models
from odoo.exceptions import UserError


class ProductReplenish(models.TransientModel):
    _inherit = "product.replenish"

    def launch_replenishment(self):
        if not self.route_id:
            raise UserError(_("You need to select a route to replenish your products"))
        if not self.route_id.rule_ids.filtered(lambda x: x.action == "manufacture"):
            return super().launch_replenishment()
        bom = self.env["mrp.bom"]._bom_find(self.product_id).get(self.product_id)
        if not bom:
            return super().launch_replenishment()
        if self.quantity < bom.product_min_qty:
            message = _(
                f"The quantity to order ({self.quantity}) is less than the minimum required ({bom.product_min_qty})."
            )
            if self.env.user.has_group("mrp.group_mrp_manager"):
                notification = super().launch_replenishment()
                notification["params"]["message"] += f" ({message})"
                notification["params"]["type"] = "warning"
                return notification
            else:
                raise UserError(message=message)
        return super().launch_replenishment()
