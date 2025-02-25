from odoo import fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warranty_linked_with_product_id = fields.Many2one("sale.order.line", ondelete="cascade")
