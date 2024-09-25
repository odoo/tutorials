from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warranty_product_id = fields.Many2one("sale.order.line", string="Warranty Product")

    def unlink(self):
        for line in self:
            warranty_product_id = self.search([("warranty_product_id", "=", line.id)])
            if warranty_product_id:
                warranty_product_id.unlink()
        return super().unlink()
