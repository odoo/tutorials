from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(related="product_template_id.is_kit")
    extra_price = fields.Float(default=0.0)
    is_subproduct = fields.Boolean()
    kit_line_id = fields.Many2one("sale.order.line")
    subproduct_line_ids = fields.One2many(
        "sale.order.line", "kit_line_id", string="Subproducts"
    )

    @api.model
    def unlink(self):
        for line in self:
            subproducts = line.subproduct_line_ids.filtered(lambda l: l not in self)
            if subproducts:
                subproducts.unlink()
        return super().unlink()

    def action_open_kit(self):
        """Open the Kit Wizard for this Sale Order Line"""
        return {
            "type": "ir.actions.act_window",
            "name": "Product Kit",
            "res_model": "product.kit.wizard",
            "target": "new",
            "view_mode": "form",
            "context": {
                "default_product_id": self.product_id.id,
                "default_sale_order_id": self.order_id.id,
                "default_kit_line_id": self.id,
            },
        }
