from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    print_in_report = fields.Boolean(string="Print In Report")

    def _get_order_lines_to_report(self):
        lines = super()._get_order_lines_to_report()

        if not self.print_in_report:
            lines = lines.filtered(lambda l: not l.linked_line_id)
        return lines
