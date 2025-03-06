from odoo import fields, models


class AccountEdiFormat(models.Model):
    _inherit = "account.edi.format"

    def _get_l10n_in_edi_line_details(self, index, line, line_tax_details):
        """
        Extend the method to set the quantity to zero if the l10n_in_is_zero_quantity field is True.

        :param index: Line index in the EDI data.
        :param line: The account.move.line record.
        :param line_tax_details: Tax details associated with the line.
        :return: Updated line details for EDI.
        """
        data = super()._get_l10n_in_edi_line_details(index, line, line_tax_details)
        if line.l10n_in_is_zero_quantity:
            data['Qty'] = 0
        return data
