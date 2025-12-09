from odoo import models


class AccountEdiFormat(models.Model):
    _inherit = "account.edi.format"

    def _get_l10n_in_edi_line_details(self, index, line, line_tax_details):
        res = super()._get_l10n_in_edi_line_details(index, line, line_tax_details)
        if line.is_zero_quantity:
            res['Qty'] = 0
        return res
