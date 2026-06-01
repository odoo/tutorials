from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_l10n_in_edi_line_details(self, index, line, line_tax_details):
        res = super()._get_l10n_in_edi_line_details(index, line, line_tax_details)

        if line.zero_move:
            res['Qty'] = 0

        return res
