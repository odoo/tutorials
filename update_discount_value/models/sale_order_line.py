from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_discount_line = fields.Boolean(default=False)

    @api.model_create_multi
    def create(self, vals):
        line = super().create(vals)
        discount_product = self.env.company.sale_discount_product_id
        if discount_product and line.product_id == discount_product:
            line.is_discount_line = True


    def unlink(self):
        orders = self.mapped("order_id")
        res = super().unlink()

        for order in orders:
            product_lines = order.order_line.filtered(lambda l: not l.is_discount_line)

            if not product_lines:
                discount_line = order.order_line.filtered(lambda l: l.is_discount_line)
                if discount_line:
                    discount_line.unlink()

        return res
