# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    show_warranty_wizard = fields.Boolean(store=False, compute="_compute_show_warranty_wizard")

    @api.depends("order_line.product_id")
    def _compute_show_warranty_wizard(self):
        for order in self:
            order.show_warranty_wizard = any(
                order_line.product_id.is_warranty_available for order_line in order.order_line
            )

    def action_open_warranty_wizard(self):
        self.ensure_one()
        return {
            "name": _("Add Warranty"),
            "type": "ir.actions.act_window",
            "res_model": "sale.order.warranty",
            "view_mode": "form",
            "target": "new",
        }
