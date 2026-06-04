from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(related='product_template_id.is_kit')
    parent_kit_line_id = fields.Many2one(
        "sale.order.line",
        ondelete="cascade",
    )
    child_kit_line_ids = fields.One2many(
        "sale.order.line",
        "parent_kit_line_id",
    )
    is_kit_child = fields.Boolean()
    kit_component_price = fields.Float()
