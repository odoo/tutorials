from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_mark_as_sold(self):
        res = super().action_mark_as_sold()
        # journal = self.env['account.journal'].search(
        #     [('type', '=', 'sale')], limit=1
        # )
        # if not journal:
        #     raise exceptions.UserError(
        #         "Please define a 'Sale' journal in Accounting settings."
        #     )

        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            # 'journal_id': journal.id,
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price
                }),
                Command.create({
                    'name': "Stella",
                    'quantity': 1,
                    'price_unit': 0.06 * self.selling_price
                }),
                Command.create({
                    'name': "Additional Fees",
                    'quantity': 1,
                    'price_unit': 100.00
                })
            ]
        })
        return res
