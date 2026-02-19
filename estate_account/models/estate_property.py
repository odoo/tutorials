# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):

        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id,
            'line_ids': [
                # 6% of the selling price
                (0, 0, {
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                # 100.00 from administrative fees
                (0, 0, {
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00,
                }),

            ],
        })

        return super().action_sold()
