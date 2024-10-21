from odoo import models, Command
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        if not (self.buyer and self.selling_price):
            raise UserError('Customer or selling price was not set.')

        commission = self.selling_price * 0.06
        fees = 100.00

        invoice_lines = [
            Command.create({'name': 'Commission (6% of the price)', 'price_unit': commission, 'quantity': 1}),
            Command.create({'name': 'Administrative fees', 'price_unit': fees, 'quantity': 1}),
        ]

        journal = self.env['account.journal'].search([('type', '=', 'sale')])

        self.env['account.move'].create({
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': invoice_lines,
            'journal_id': journal.id,
        })

        return super().action_sold()
