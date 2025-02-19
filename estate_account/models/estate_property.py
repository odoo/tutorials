from odoo import models, fields, Command
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        move_type = 'out_invoice'
        journals = self.env['account.journal'].search([])
        if len(journals) == 0:
            raise UserError("Please define an accounting journal")
        invoice_vals = {
            'partner_id': self.buyer_id.id,
            'move_type': move_type,
            'journal_id': journals[0].id,
            'invoice_line_ids': [
                Command.create({
                    'name': '6% of the selling price',
                    'quantity': 1.0,
                    'price_unit': .06 * self.selling_price,
                }),
                Command.create({
                    'name': 'additional 100.00 from administrative fees',
                    'quantity': 1.0,
                    'price_unit': 100.0,
                }),
            ],
        }
        self.env['account.move'].create([invoice_vals])
        return super().action_sold()
