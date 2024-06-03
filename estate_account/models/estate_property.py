# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sell(self):
        """
        Create an invoice when a property is sold.
        """
        res = super().action_sell()
        self.check_access_rights('write')
        self.check_access_rule('write')
        for record in self:
            invoice_lines = [
                Command.create(line)
                for line in [
                    {
                        'name': 'Down-payment',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    },
                    {'name': 'Administrative fees', 'quantity': 1, 'price_unit': 100.00},
                ]
            ]
            self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(
                {
                    'partner_id': record.buyer_id.id,
                    'move_type': 'out_invoice',
                    'line_ids': invoice_lines,
                }
            )
        return res
