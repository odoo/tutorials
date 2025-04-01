from odoo import models, api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def is_discount_line(self):
        discount_product = self.order_id.env["product.product"].search([("name", "=", "Discount")], limit=1)
        return self.product_id == discount_product
    
    def unlink(self):
        order_ids = self.mapped("order_id")
        res = super().unlink()

        for order in order_ids:
            order._update_discount()
        return res

    @api.model_create_multi
    def create(self, vals):
        line = super().create(vals)

        if line.order_id and not line.is_discount_line():
            line.order_id._update_discount()

        return line
