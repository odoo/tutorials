from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

     # Linking to the product warranty
    product_warranty_id = fields.Many2one(
        "product.product",
        string="Warranty Configuration",
    )

    def unlink(self):
        for line in self:
            # If product delete than associated warranty delete
            warranty_lines = self.env["sale.order.line"].search(
                [("product_warranty_id", "=", line.product_id.id)]
            )

            if warranty_lines:
                warranty_lines.unlink()
        return super(SaleOrderLine, self).unlink()
