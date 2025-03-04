# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models
from odoo.exceptions import UserError


class SaleOrderDiscount(models.TransientModel):
    _inherit = "sale.order.discount"

    def _create_discount_lines(self):
        if self.discount_type == "so_discount":
            if self.sale_order_id.global_discount_percentage:
                raise UserError("A global discount has already been applied.")
            if self.discount_percentage <= 0:
                raise UserError("Discount percentage must be greater than 0.")
        res = super()._create_discount_lines()
        if self.discount_type == "so_discount":
            self.sale_order_id.global_discount_percentage = self.discount_percentage
            res.write({"is_global_discount_line": True})
        return res
