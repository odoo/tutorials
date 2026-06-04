from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    has_kit_products = fields.Boolean(
        compute='_compute_has_kit_products',
        store=False
    )

    print_kit_in_report = fields.Boolean(
        string="Print Kit Components in Report",
        default=False
    )

    @api.depends('order_line.is_kit_line')
    def _compute_has_kit_products(self):
        for order in self:
            order.has_kit_products = any(line.is_kit_line for line in order.order_line)
