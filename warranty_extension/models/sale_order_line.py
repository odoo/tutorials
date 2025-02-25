from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warranty_id = fields.Many2one("warranty.configuration",string="Warranty")
    linked_order_line_id = fields.Many2one("sale.order.line", string="Linked Product Line", ondelete="cascade")
