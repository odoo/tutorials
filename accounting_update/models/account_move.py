from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_l10n_in_edi_line_details(self, index, line, line_tax_details):
        line_details = super()._get_l10n_in_edi_line_details(
            index, line, line_tax_details
        )
        if line.is_zero_qty:
            line_details["Qty"] = 0.0
        return line_details
