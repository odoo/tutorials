from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def show_in_report(self):
        self.ensure_one()

        sale_line = self.sale_line_ids[:1]

        return (
            not sale_line.is_kit_product
            or sale_line.order_id.print_in_report
        )
