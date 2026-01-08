from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warranty_id = fields.Many2one(
        "warranty.configuration",
        string="Warranty",
        help="Warranty applied to this product line."
    )

    linked_order_line_id = fields.Many2one(
        "sale.order.line",
        string="Linked Product Line",
        help="The product line this warranty applies to.",
        ondelete="cascade"
    )
