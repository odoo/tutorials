# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    print_sub_products_in_report = fields.Boolean(
        string="Print in report?", help="Print sub product in report as well as in customer preview"
    )

    def _get_order_lines_to_report(self):
        order_lines_to_report = super()._get_order_lines_to_report()
        return order_lines_to_report.filtered(lambda line: not line.parent_kit_line_id or self.print_sub_products_in_report)
