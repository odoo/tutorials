from odoo import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    kit_parent_id = fields.Many2one(
        "sale.order.line", string="Kit Parent Line", ondelete="cascade"
    )

    is_kit_product = fields.Boolean(
        string="Is Kit Product", compute="_compute_is_kit_product", store=False
    )

    @api.depends("product_id")
    def _compute_is_kit_product(self):
        for line in self:
            line.is_kit_product = (
                line.product_id.product_tmpl_id.is_kit if line.product_id else False
            )
