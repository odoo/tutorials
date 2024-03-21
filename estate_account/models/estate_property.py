# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        values = {
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            #'journal_id': self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id
            'invoice_line_ids': [
                Command.create({
                    'name': self.name + ' - 6% down payment',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                Command.create({
                    'name': 'administrative fees',
                    'quantity': 1,
                    'price_unit': 100.00,
                }),
            ]
        }
        self.env['account.move'].create(values)
        return super().action_sold()
