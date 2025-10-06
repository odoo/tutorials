from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    linked_to_warranty_id = fields.Many2one("sale.order.line", ondelete="cascade")

    def unlink(self):
        for line in self:
            if line.linked_to_warranty_id:
                warranties = self.env["sale.order.line"].search([("linked_to_warranty_id", "=", line.id)])
                warranties.unlink()
        return super(SaleOrderLine, self).unlink()
