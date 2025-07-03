from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_is_kit = fields.Boolean(
        compute="_compute_product_is_kit",
    )
    parent_kit_id = fields.Many2one("sale.order.line")
    original_price_unit = fields.Float()

    @api.depends("product_id")
    def _compute_product_is_kit(self):
        for line in self:
            line.product_is_kit = line.product_id.product_tmpl_id.is_kit
            if not line.original_price_unit:
                line.original_price_unit = line.price_unit

    def open_sub_prod(self):
        return {
            "name": f"Product : {self.product_id.display_name}",
            "type": "ir.actions.act_window",
            "res_model": "sale.sub.product.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"active_id": self.id},
        }
