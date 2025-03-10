from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    related_product_id = fields.Many2one("product.template", "Related Main Product", default=False)

    def unlink(self):
        for line in self:
            if line.product_id:
                self.order_id.order_line.filtered(
                    lambda l: l.related_product_id == line.product_template_id
                ).unlink()
        return super(SaleOrderLine, self).unlink()
