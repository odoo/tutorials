from odoo import models, Command


class InheritedEstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):

        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)

        created_invoice = self.env["account.move"].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': journal.id,
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price * 1.06
                })
            ]
        })

        return super().action_set_sold()
