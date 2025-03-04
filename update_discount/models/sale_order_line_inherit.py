from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def write(self, vals):
        if self.env.context.get("suppress_write"):
            return super(SaleOrderLine, self).write(vals)

        res = super(SaleOrderLine, self).write(vals)

        for line in self:
            if line.order_id and not line.is_discount_line():
                line.order_id.with_context(
                    suppress_write=True
                )._add_or_update_discount()
        return res

    def unlink(self):
        order_ids = self.mapped("order_id")
        res = super(SaleOrderLine, self).unlink()

        for order in order_ids:
            order.with_context(suppress_write=True)._add_or_update_discount()
        return res

    def is_discount_line(self):
        discount_product = self.order_id._get_discount_product()
        return self.product_id == discount_product
