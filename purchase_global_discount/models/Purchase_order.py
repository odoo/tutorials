from odoo import fields, models, api


class PurchaseGlobalDiscount(models.Model):
    _inherit = "purchase.order"

    total_price_without_discount = fields.Float(
        string="Total Price Without Discount",
        compute="_compute_total_price_without_discount",
        store=True,
    )

    global_discount = fields.Float(string="Discount ", store=True, default=0)
    global_discount_type = fields.Selection(
        [
            ("percent", "%"),
            ("amount", "$"),
        ],
        string="Discount Type",
        default="percent",
        store=True,
    )
    computed_percentage = fields.Float(
        string="Discount %", compute="_compute_percentage", default=0
    )

    @api.depends(
        "global_discount", "global_discount_type", "total_price_without_discount"
    )
    def _compute_percentage(self):
        for records in self:
            if records.global_discount_type == "amount" and records.global_discount > 0:
                records.computed_percentage = (
                    records.global_discount * 100
                ) / records.total_price_without_discount
            elif records.global_discount_type == "percent":
                records.computed_percentage = records.global_discount
            else:
                records.computed_percentage = 0

    @api.depends("order_line.price_unit", "order_line.product_qty")
    def _compute_total_price_without_discount(self):
        for order in self:
            total = 0.0
            for line in order.order_line:
                total += line.product_qty * line.price_unit
            order.total_price_without_discount = total

    def action_apply(self):
        if self.computed_percentage > 0:
            self.order_line.discount = self.computed_percentage

    def action_discount(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Discount",
            "res_model": "purchase.order",
            "view_type": "form",
            "view_mode": "form",
            "view_id": self.env.ref(
                "purchase_global_discount.view_purchase_global_discount_form"
            ).id,
            "res_id": self.id,
            "target": "new",
        }
