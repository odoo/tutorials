from odoo import fields, models


class salesOrderLine(models.Model):
    _inherit = "sale.order.line"

    linked_sale_order_line_id = fields.Many2one(
        "sale.order.line", string="Linked Product Line"
    )

    def unlink(self):
        for line in self:
            linked_warranty_lines = self.search(
                [("linked_sale_order_line_id", "=", line.id)]
            )

            linked_warranty_lines.unlink()

        return super().unlink()
