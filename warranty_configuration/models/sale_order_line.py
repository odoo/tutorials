from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    parent_sale_order_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        readonly=True,
        ondelete="cascade",
        string="parent sale order line id",
    )
