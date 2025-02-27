# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warranty_line_ids = fields.One2many(
        comodel_name="sale.order.line",
        inverse_name="warranty_parent_line_id",
        help="Lines representing warranties associated with this product line."
    )
    warranty_parent_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        ondelete="cascade",
        help="The original product line that this warranty line covers."
    )
