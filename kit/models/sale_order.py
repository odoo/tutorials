from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    print_sub_products_in_report = fields.Boolean(string="Print in report?")

    def _get_order_lines_to_report(self):
        all_lines = super(SaleOrder, self)._get_order_lines_to_report()
        if all_lines and not self.print_sub_products_in_report:
            filtered_lines = all_lines.filtered(lambda line: not line.parent_id)
            return filtered_lines
        return all_lines
