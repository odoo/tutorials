from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_is_kit = fields.Boolean(
        related="product_id.product_tmpl_id.is_kit",
    )

    parent_kit_line_id = fields.Many2one(
        "sale.order.line",
        string="Parent Kit Line",
        ondelete="cascade",
        copy=False,
    )

    sub_product_line_ids = fields.One2many(
        "sale.order.line", "parent_kit_line_id", string="Sub-product Lines", copy=False
    )

    is_kit_sub_product = fields.Boolean(string="Is a Kit Sub-product", copy=False)

    def open_sub_product_wizard(self):
        return {
            "name": f"Product : {self.product_id.display_name}",
            "type": "ir.actions.act_window",
            "res_model": "sub.products.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"active_id": self.id},
        }
