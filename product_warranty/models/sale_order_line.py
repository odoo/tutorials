from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    link_product_id = fields.Many2one("sale.order.line", ondelete="cascade")
