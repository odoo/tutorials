from datetime import timedelta

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    delivery_date = fields.Date(string='Delivery Date')

    def action_post(self):
        res = super().action_post()
        for move in self:
            if move.move_type == 'out_invoice':
                move.delivery_date = fields.Date.today() + timedelta(days=7)

        return res
