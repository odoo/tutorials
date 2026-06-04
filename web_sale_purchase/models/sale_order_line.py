from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    seller_id = fields.Many2one("res.partner", related="product_id.seller_id")
