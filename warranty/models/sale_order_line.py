from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    waranty_with_products = fields.Many2one("sale.order.line")

    def unlink(self):
        for line in self:
            warranty_lines = self.env["sale.order.line"].search(
                [("waranty_with_products", "=", line.id)]
            )
            if warranty_lines:
                warranty_lines.unlink()

        return super().unlink()
