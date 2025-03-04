from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(related="product_template_id.is_kit")
    price_current = fields.Float(string="Price", default=0.0)
    is_subproduct = fields.Boolean(string="Is Subproduct")
    parent_line_id = fields.Many2one(
        comodel_name="sale.order.line", string="Parent Line"
    )

    def action_product_subproduct_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Add Sub Products",
            "res_model": "subproducts.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "active_id": self.order_id.id,
                "default_product_id": self.product_id.id,
                "default_parent_id": self.id,
            },
        }

    @api.model
    def unlink(self):
        for line in self:
            sub_lines = self.env["sale.order.line"].search([("parent_line_id", "=", line.id)]).filtered(lambda l: l not in self)
            if sub_lines:
                sub_lines.unlink()

        return super().unlink()
