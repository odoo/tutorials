from odoo import api, models


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
        lines = super().create(vals)
        for line in lines:
            if line.order_id and not line.is_discount_line():
                line.order_id._update_discount()
        return lines

    def write(self, vals):
        res = super().write(vals)
        for line in self:
            if not line.is_discount_line():
                line.order_id._update_discount()
        return res
