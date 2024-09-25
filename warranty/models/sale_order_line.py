from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warranty_product_line_id = fields.Many2one(
        "sale.order.line", string="Warranty Product Line"
    )

    def unlink(self):
        for line in self:
            warranty_product_ids = self.env["sale.order.line"].search(
                [("warranty_product_line_id", "=", line.id)]
            )

            if warranty_product_ids:
                warranty_product_ids.unlink()

        return super().unlink()
