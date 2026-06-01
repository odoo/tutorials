from odoo import fields, models


class ZeroAccountMove(models.Model):
    _inherit = 'account.move.line'

    zero_move = fields.Boolean(string="Is Zero Quantity", default=False)
