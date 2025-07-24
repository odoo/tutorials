from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    # Use the same field name as on your sale.order for consistency
    is_printable_kit = fields.Boolean(string="Show Sub-Products", default=True)
