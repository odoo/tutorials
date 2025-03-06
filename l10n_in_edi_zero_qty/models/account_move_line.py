from odoo import fields, models


class AccountMoveLine(models.Model):
    """
    Extension of the 'account.move.line' model to add a custom field.
    """
    _inherit = 'account.move.line'

    l10n_in_is_zero_quantity = fields.Boolean(
        string="Is Zero Quantity",
        help="When checked, the product quantity for this line will be set to zero."
    )
