from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    connected_order_line_id = fields.Many2one("sale.order.line", ondelete="cascade")
