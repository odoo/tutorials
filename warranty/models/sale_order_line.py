from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
