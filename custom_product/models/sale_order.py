from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # is_kit_component = fields.Boolean(string="Kit Component", default=False)
    kit_parent_id = fields.Many2one(
        "sale.order.line", string="Kit Parent Line", ondelete="cascade"
    )
    kit_child_line_ids = fields.One2many(
        "sale.order.line", "kit_parent_id", string="Kit Child Lines", ondelete="cascade"
    )
