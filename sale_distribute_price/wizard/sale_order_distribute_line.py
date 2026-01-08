from odoo import api, fields, models

class SaleOrderDistributeLine(models.TransientModel):
    _name = "sale.order.distribute.line"
    _description = "Sale Order Distribute Line"

    wizard_id = fields.Many2one("sale.order.distribute", required=True)
    order_line_id = fields.Many2one("sale.order.line", required=True)
    product_id = fields.Many2one("product.product")
    amount = fields.Float(string="Amount")
    is_divided = fields.Boolean(string="Divide?")

    @api.onchange("is_divided")
    def _onchange_is_divided(self):
        if not self.is_divided:
            self.amount = 0.0
