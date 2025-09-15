from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warranty_line_linked_with_so_line = fields.Many2one(
        "sale.order.line", ondelete="cascade"
    )
