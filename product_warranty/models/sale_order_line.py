from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warranty_id = fields.Many2one(
        "product.warranty",
        string="Warranty",
        help="Warranty applied to this product line."
    )
