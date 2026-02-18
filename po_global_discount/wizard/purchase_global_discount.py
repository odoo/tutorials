from odoo import api, fields, models
from odoo.exceptions import UserError


class PurchaseGlobalDiscount(models.TransientModel):
    _name = 'purchase.global.discount'

    order_id = fields.Many2one('purchase.order', required=True)
    discount_value = fields.Float()
    discount_type = fields.Selection(
        [
            ("percentage", "%"),
            ("amount", "$"),
        ],
        default="percentage"
    )
    discount_percentage = fields.Float(compute="_compute_discount_percentage", string="Preview Percentage")

    @api.depends('discount_value', 'discount_type', 'order_id')
    def _compute_discount_percentage(self):
        for wizard in self:
            wizard.discount_percentage = 0.0
            if wizard.discount_type == 'percentage':
                wizard.discount_percentage = wizard.discount_value
            elif wizard.discount_type == 'amount' and wizard.order_id:
                total_amount = sum(line.price_unit * line.product_qty for line in wizard.order_id.order_line)
                if total_amount > 0:
                    wizard.discount_percentage = (wizard.discount_value / total_amount) * 100

    def action_apply_discount(self):
        self.ensure_one()
        if self.discount_percentage > 100:
            raise UserError("Discount Must be less then 100% ")
        for line in self.order_id.order_line:
            line.discount = self.discount_percentage
        return {'type': 'ir.actions.act_window_close'}
