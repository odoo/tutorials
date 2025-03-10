from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("order_line")
    def _onchange_order_line_price_unit(self):
        for line in self.order_line.filtered(lambda l: not l.product_warranty_line_id):

            if line.product_id.is_warranty_available:
                # Find the corresponding warranty product lines
                warranty_lines = self.order_line.filtered(
                    lambda ln: ln.product_warranty_line_id.product_id == line.product_id
                )
                for warranty_line in warranty_lines:
                    warranty_config = self.env["warranty.configuration"].search(
                        [("product_id", "=", warranty_line.product_id.id)], limit=1
                    )

                    if warranty_config:
                        new_warranty_price = (
                            line.price_unit * warranty_config.percentage / 100
                        )
                        # Update warranty product's price_unit
                        warranty_line.price_unit = new_warranty_price
