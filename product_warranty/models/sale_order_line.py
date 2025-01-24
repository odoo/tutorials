from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    deposit_link_product_id = fields.Integer()

    @api.ondelete(at_uninstall=False)
    def _unlink_if_no_product(self):
        if self.product_id.is_warranty:
            deposit_linked = self.env["sale.order.line"].search(
                [
                    ("deposit_link_product_id", "=", self.id),
                    ("order_id", "=", self.order_id.id),
                ]
            )
            for unlink in deposit_linked:
                unlink.unlink()
