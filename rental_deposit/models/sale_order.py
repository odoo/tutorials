from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def copy(self, default=None):
        """Override copy to prevent deposit lines from being duplicated."""
        default = dict(default or {})

        deposit_product_id = self.env["ir.config_parameter"].sudo().get_param("rental_deposit.deposit_product_id")

        filtered_lines = self.order_line.filtered(lambda line: not line.product_id.id == int(deposit_product_id))

        default["order_line"] = [(0, 0, line.copy_data()[0]) for line in filtered_lines]

        return super().copy(default)
