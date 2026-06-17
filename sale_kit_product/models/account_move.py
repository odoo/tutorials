from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_move_lines_to_report(self):
        lines = super()._get_move_lines_to_report()
        return lines.filtered(
            lambda l: (
                not l.sale_line_ids.is_sub_product
                or l.sale_line_ids.order_id.print_in_report
            )
        )
