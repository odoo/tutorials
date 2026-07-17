from odoo import fields, models


class AccountMove(models.Model):
    """Add a link from invoices back to the estate property that generated them.

    This allows the invoice form to show which property triggered the invoice
    creation, which is useful for reconciliation and accounting reports.
    """
    _inherit = 'account.move'

    # -----------------------------------------------------------------------
    # Fields
    # -----------------------------------------------------------------------
    estate_property_id = fields.Many2one(
        'awesome.estate.property',
        string="Property",
        ondelete='restrict',
        index=True,
        help="The real estate property that generated this invoice.",
    )
