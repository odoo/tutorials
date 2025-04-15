from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(related="product_template_id.is_kit")
    is_sub_product_ol = fields.Boolean()
    main_order_line_id = fields.Many2one(
        "sale.order.line",
        string="Parent Line",
        ondelete="cascade",
    )

    child_line_ids = fields.One2many(
        "sale.order.line",
        "main_order_line_id",
        string="Child Lines",
    )
    display_price = fields.Float(
        compute="_compute_display_price", inverse="_compute_unit_price"
    )
    display_sub_total = fields.Float(compute="_compute_amount_price")

    @api.depends("price_unit", "is_sub_product_ol")
    def _compute_display_price(self):
        for line in self:
            line.display_price = 0.0 if line.is_sub_product_ol else line.price_unit

    @api.depends("display_price", "price_subtotal", "is_sub_product_ol")
    def _compute_amount_price(self):
        for line in self:
            line.display_sub_total = (
                0.0 if line.is_sub_product_ol else line.price_subtotal
            )

    def _compute_unit_price(self):
        for line in self:
            line.price_unit = line.display_price

    def unlink(self):
        for line in self:
            line.main_order_line_id.price_subtotal -= (
                line.product_uom_qty * line.price_unit
            )

        return super().unlink()

    def open_sub_product_wizard(self):
        return {
            "name": "Sale order line wizard action",
            "type": "ir.actions.act_window",
            "res_model": "sale.order.line.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"active_id": self.id},
        }
