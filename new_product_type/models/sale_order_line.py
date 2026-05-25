from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(
        related="product_id.product_tmpl_id.is_kit",
        store=True
    )
    is_kit_product = fields.Boolean()
    kit_parent_line_id = fields.Many2one("sale.order.line", ondelete="cascade")
    extra_price = fields.Float(default=0.0)

    @api.ondelete(at_uninstall=False)
    def _check_kit_product_restriction(self):
        for line in self:
            if line.is_kit_product:
                raise UserError(_("You cannot delete a kit sub product directly."))

    def show_in_report(self):
        self.ensure_one()
        return (
            not self.is_kit_product
            or self.order_id.print_in_report
        )

    def action_open_kit_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Configure Kit",
            "res_model": "product.kit.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "active_id": self.id
            },
        }
