from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warranty_line_id = fields.Many2one("sale.order.line", ondelete="cascade")
    warranty_id = fields.Many2one('product.warranty', string="Warranty")
