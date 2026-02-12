from odoo import models, fields, _
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(related="product_id.product_tmpl_id.is_kit", store=True)
    is_kit_product = fields.Boolean()
    kit_parent_line_id = fields.Many2one("sale.order.line")
    extra_price = fields.Float(default=0.0)

    def unlink(self):
        parents_in_self = self.filtered(lambda l: not l.is_kit_product)
        # parents = self.env["sale.order.line"].search([
        #     ("id", "in", self.ids),
        #     ("is_kit_product", "=", False),
        # ])
        children_in_self = self.filtered(lambda l: l.is_kit_product)
        for child in children_in_self:
            if child.kit_parent_line_id not in parents_in_self:
                raise UserError(_("You cannot delete a kit sub product directly."))
        child_lines = self.search([
            ("kit_parent_line_id", "in", parents_in_self.ids)
        ])
        if child_lines:
            child_lines.unlink()
        return super().unlink()

    def action_open_kit_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Configure Kit",
            "res_model": "product.kit.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"active_id": self.id},
        }
