from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(
        related='product_template_id.is_kit',
        store=True,
        default=False
    )

    parent_id = fields.Many2one(
        'sale.order.line',
        ondelete='cascade'
    )

    kit_price = fields.Float()
