from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"
    penalty_applied = fields.Boolean(string="Penalty Applied", default=False)
