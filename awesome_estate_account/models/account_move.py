from odoo import fields, models


class AccountMove(models.Model):
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
