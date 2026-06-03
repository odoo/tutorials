from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_zero_qty = fields.Boolean()
