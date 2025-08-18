from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    is_printable_kit = fields.Boolean(string="Show Sub-Products", default=True)
