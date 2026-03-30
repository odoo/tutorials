from odoo import api, fields, models


class PurchaseOrderDiscount(models.TransientModel):
    _name = "purchase.order.discount"
    _description = "Purchase Discount Wizard"

    purchase_order_id = fields.Many2one(
        "purchase.order",
        default=lambda self: self.env.context.get("default_purchase_order_id"),
        required=True,
    )
    company_id = fields.Many2one(related="purchase_order_id.company_id")
    currency_id = fields.Many2one(related="purchase_order_id.currency_id")
    discount_amount = fields.Monetary(string="Amount")
    discount_percentage = fields.Float(string="Percentage")
    discount_type = fields.Selection(
        string="Discount Type",
        selection=[
            ("percentage", "Percentage"),
            ("amount", "Fixed Amount"),
        ],
        default="percentage",
        required=True,
    )
    discount_amount_percentage = fields.Float(
        string="Amount %", compute="_compute_discount_amount_percentage", store=True
    )

    @api.depends("discount_amount")
    def _compute_discount_amount_percentage(self):
        for record in self:
            order = record.purchase_order_id
            total = sum(line.price_unit * line.product_qty for line in order.order_line)
            if total:
                record.discount_amount_percentage = record.discount_amount / total
            else:
                record.discount_amount_percentage = 0.0

    def action_apply_discount(self):
        self.ensure_one()
        order = self.purchase_order_id

        if self.discount_type == "percentage":
            for line in order.order_line:
                line.discount = self.discount_percentage * 100
        elif self.discount_type == "amount":
            self._apply_fixed_amount_discount()

    def _apply_fixed_amount_discount(self):
        order = self.purchase_order_id
        for line in order.order_line:
            line.discount = 0.0
            if self.discount_amount_percentage:
                line.discount = self.discount_amount_percentage * 100
