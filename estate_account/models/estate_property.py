from odoo import models, Command


class InheritedEstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        invoices = []
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        for estate in self:
            invoice = {
                'partner_id': estate.buyer_id.id,
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                'line_ids': [
                    Command.create(
                        {
                            'name': estate.name,
                            'quantity': 1,
                            'price_unit': 0.06 * estate.selling_price,
                        }
                    ),
                    Command.create(
                        {
                            'name': 'Administrative fees',
                            'quantity': 1,
                            'price_unit': 100,
                        }
                    ),
                ],
            }

            invoices.append(invoice)

        self.env['account.move'].create(invoices)

        return super().action_sold()
