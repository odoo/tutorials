from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    have_module_types = fields.Integer(
        compute="_compute_module_types_count"
    )

    @api.depends('product_template_id.module_types')
    def _compute_module_types_count(self):
        for line in self:
            line.have_module_types = bool(line.product_id.module_types)
