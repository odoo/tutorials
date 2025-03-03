from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(related="product_template_id.is_kit")
    kit_parent_id = fields.Many2one("sale.order.line")
    is_kit_component = fields.Boolean()
    extra_price = fields.Float(default=0.0)

    def open_kit_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Kit Configuration",
            "res_model": "sub.product.kit.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"active_id": self.id},
        }

    def unlink(self):
        child_lines = self.env["sale.order.line"].search([("kit_parent_id", "in", self.ids)])
        for line in self:
            if not line.kit_parent_id:
                child_lines.filtered(lambda l: l not in self).unlink()

        return super().unlink()
