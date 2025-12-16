from odoo import models, Command


class EstateAccount(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        for record in self:
            partner_id = record.buyer.id
            move_type = 'out_invoice'
            journal_id = self.env['account.journal'].search([("type", "=", 'sale')], limit=1).id
            self.env['account.move'].create({
                'partner_id': partner_id,
                'move_type': move_type,
                'journal_id': journal_id,
                'invoice_line_ids': [
                    Command.create({
                        'name': "Brokerage Fee",
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': "Administrative Fee",
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ]
            })
        return super().action_set_sold()
