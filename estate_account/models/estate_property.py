from odoo import models
from odoo.exceptions import UserError
from odoo.orm.commands import Command

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sell(self):

        journal = self.env['account.journal'].search([('type', 'in', 'sale')], limit=1)
        invoice_vals = []

        for record in self:
            invoice_vals.append({
                'name': record.name,
                'partner_id': record.partner_id.id,
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': record.name,
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ]
            })

        self.env['account.move'].create(invoice_vals)

        return super().action_sell()
