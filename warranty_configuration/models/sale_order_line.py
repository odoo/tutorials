from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_warranty_line_id = fields.Many2one(
        "sale.order.line",
        string="Parent product for warranty",
        ondelete="cascade",
    )  # Parent product for warranty
