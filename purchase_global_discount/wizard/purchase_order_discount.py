from odoo import api, fields, models


class PurchaseOrderDiscount(models.TransientModel):
    _name = "purchase.order.discount"
    _description = "Discount Wizard"

    purchase_order_id = fields.Many2one(
        'purchase.order', default=lambda self: self.env.context.get('active_id'), required=True)
    company_id = fields.Many2one(related='purchase_order_id.company_id')
    currency_id = fields.Many2one(related='purchase_order_id.currency_id')
    discount_amount = fields.Monetary(string="Amount")
    discount_percentage = fields.Float(string="Percentage")
    discount_type = fields.Selection([
        ('amount', "Amount (Total)"),
        ('percentage', "Percentage"),
    ], default='percentage')

    def _get_original_total(self):
        return sum(
            line.price_unit * line.product_qty
            for line in self.purchase_order_id.order_line
        )

    @api.onchange('discount_amount')
    def _onchange_discount_amount(self):
        original_total = self._get_original_total()
        if original_total:
            self.discount_percentage = (self.discount_amount / original_total)

    def action_apply_discount(self):
        self.ensure_one()
        self.purchase_order_id.order_line.write({'discount': self.discount_percentage * 100})
