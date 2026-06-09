from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_sub_product = fields.Boolean()
    parent_kit_line_id = fields.Many2one("sale.order.line", ondelete="cascade")
    kit_line_ids = fields.One2many("sale.order.line", "parent_kit_line_id")
