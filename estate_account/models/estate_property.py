from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()

        journal = self.env['account.journal'].search(
            [('type', '=', 'sale')],
            limit=1
        )

        for property in self:
            self.env['account.move'].create({
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': 'Commission (6%)',
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ],
            })
        return res
